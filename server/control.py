import time
from enum import Enum
from typing import Optional

import ik
import numpy as np
import protocol
from motor import MotorContext

STEPS = 3200


def angle_to_step(angle):
    steps_per_rotation = STEPS
    steps = round(angle / (2 * np.pi) * steps_per_rotation)
    return steps


def mapSteps(v: int, prev: int | None) -> int:
    if prev == None:
        return v

    diff = np.abs(prev - v)

    if diff > (STEPS / 2):
        v = v - STEPS

    return v


class Command(Enum):
    screwIn = 1111
    screwOut = 2222
    moveUp = 3333
    moveDown = 4444


class Move:
    delay: float
    pos: Optional[np.ndarray]
    command: Optional[Command]

    motor1Inv: bool
    motor2Inv: bool

    def __init__(
        self,
        position: Optional[np.ndarray] = None,
        command: Optional[Command] = None,
        motor1Inv: bool = False,
        motor2Inv: bool = False,
        delay: float = 0,
    ) -> None:
        self.delay = delay
        self.pos = position

        self.motor1Inv = motor1Inv
        self.motor2Inv = motor2Inv

        self.command = command


class Control:
    node1: protocol.NodeConnection
    node2: protocol.NodeConnection
    offset_angle_motor1: float
    offset_angle_motor2: float
    motor1: MotorContext
    motor2: MotorContext

    last_steps_motor1: int | None
    last_steps_motor2: int | None

    last_position: np.ndarray

    def __init__(
        self,
        motor1: MotorContext,
        motor2: MotorContext,
        node1_conn: protocol.NodeConnection,
        node2_conn: protocol.NodeConnection,
    ) -> None:
        self.motor1 = motor1
        self.motor2 = motor2
        self.node1 = node1_conn
        self.node2 = node2_conn
        self.last_steps_motor1 = None
        self.last_steps_motor2 = None

    def setOrigin(
        self,
        motor1Inv: bool = False,
        motor2Inv: bool = False,
        offset: np.ndarray = np.array([0, 0]),
    ):
        # Sets offsets
        self.offset_angle_motor1 = ik.calc_motor_angles(
            self.motor1, np.array([0, 0]) + offset, change_dir=motor1Inv
        )[0]
        self.offset_angle_motor2 = ik.calc_motor_angles(
            self.motor2, np.array([0, 0]) + offset, change_dir=motor2Inv
        )[0]

        # self.node1.debug(
        #     "Calculated angles: ",
        #     (self.offset_angle_motor1 * 180) / np.pi,
        #     (self.offset_angle_motor2 * 180) / np.pi,
        # )

        # For setting last step in proper pos
        self._moveTo(
            np.array([0, 0]) + offset, motor1Inv=motor1Inv, motor2Inv=motor2Inv
        )

    def getSteps(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ) -> tuple[int, int]:
        motor_angle1 = ik.calc_motor_angles(
            self.motor1, coordinate, change_dir=motor1Inv
        )[0]
        motor_angle2 = ik.calc_motor_angles(
            self.motor2, coordinate, change_dir=motor2Inv
        )[0]

        # self.node1.debug(
        #     "Moving to angles: ",
        #     (motor_angle1 * 180) / np.pi,
        #     (motor_angle2 * 180) / np.pi,
        # )

        motor1_steps = angle_to_step(motor_angle1)
        motor2_steps = angle_to_step(motor_angle2)

        mapped_steps1 = mapSteps(motor1_steps, self.last_steps_motor1)
        mapped_steps2 = mapSteps(motor2_steps, self.last_steps_motor2)

        # self.node1.debug("mapped_steps:", mapped_steps1, mapped_steps2)

        self.last_steps_motor1 = mapped_steps1
        self.last_steps_motor2 = mapped_steps2

        mapped_steps1_absolute = mapped_steps1 - angle_to_step(self.offset_angle_motor1)
        mapped_steps2_absolute = mapped_steps2 - angle_to_step(self.offset_angle_motor2)

        # self.node1.debug(
        #     "relative steps: ", mapped_steps1_absolute, mapped_steps2_absolute
        # )

        return mapped_steps1_absolute, mapped_steps2_absolute

    def _moveTo(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ):
        steps1, steps2 = self.getSteps(coordinate, motor1Inv, motor2Inv)
        self.sendSteps(steps1, steps2)  # Replace with sendSteps() when using Arduino
        self.last_position = coordinate

    def moveTo(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ):
        # self._interpolatedMoveTo(
        #     self.last_position, coordinate, motor1Inv=motor1Inv, motor2Inv=motor2Inv
        # )
        self._moveTo(coordinate, motor1Inv=motor1Inv, motor2Inv=motor2Inv)
        self.node1.debug(f"Done moving to: ", coordinate)

    def sendCommand(self, command: Command):
        m = command.value.to_bytes(4, "little")
        # self.node2.debug(f"Sending: {m}")
        self.node2.writeMessage(m)
        rm = self.node2.readMessage()
        # self.node2.debug(rm)
        self.node2.debug(f"Done {command.name}!")

    def _interpolatedMoveTo(
        self,
        coordinate1: np.ndarray,
        coordinate2: np.ndarray,
        motor1Inv: bool = False,
        motor2Inv: bool = False,
    ):
        diff_vec = coordinate2 - coordinate1
        # num_steps = int(np.sqrt(diff_vec[0] ** 2 + diff_vec[1] ** 2)) * 0.5
        num_steps = 1
        for i in range(round(num_steps)):
            abs_pos = coordinate1 + (i * (diff_vec / num_steps))
            self._moveTo(abs_pos, motor1Inv=motor1Inv, motor2Inv=motor2Inv)

    def sendSteps(self, steps1: int, steps2: int):
        # Because on the Node1 side, steps are subtracted by 3200 to allow negative numbers
        absolute_steps1, absolute_steps2 = steps1 + 3200, steps2 + 3200
        # self.node1.debug(f"Going to pos: {steps1},{steps2}")

        message_buf = absolute_steps1.to_bytes(4, "little") + absolute_steps2.to_bytes(
            4, "little"
        )

        # Write command
        self.node1.writeMessage(message_buf)

        # Wait for done
        self.node1.readMessage()
        # self.node1.debug(f"Done")

    def sendStepsDebug(self, steps1: int, steps2: int):
        absolute_steps1, absolute_steps2 = steps1 + 3200, steps2 + 3200
        print(f"Going to pos: {steps1},{steps2}")

    def executeMove(self, move: Move):
        if move.delay is not None or move.delay != 0:
            self.node1.debug(f"Waiting {move.delay} seconds...")
            self.node2.debug(f"Waiting {move.delay} seconds...")
            time.sleep(move.delay)
        if move.pos is not None:
            # print("MOVE")
            self.moveTo(move.pos, motor1Inv=move.motor1Inv, motor2Inv=move.motor2Inv)
        if move.command is not None:
            # print("COMMAND")
            self.sendCommand(move.command)
