import ik
import numpy as np
import protocol
from motor import MotorContext


def angle_to_step(angle):
    steps_per_rotation = 3200
    steps = round(angle / (2 * np.pi) * steps_per_rotation)
    return steps


# def shortestAngle(previous: float, current: float) -> float:
#     # https://stackoverflow.com/questions/28036652/finding-the-shortest-distance-between-two-angles
#     diff = (previous - current + 180) % 360 - 180
#     if diff < -180:
#         return diff + 360
#     else:
#         return diff


def shortestAngle(previous: float, current: float) -> float:
    # https://stackoverflow.com/questions/28036652/finding-the-shortest-distance-between-two-angles
    diff = (previous - current + (np.pi)) % (np.pi * 2) - (np.pi)
    if diff < -(np.pi):
        return diff + (np.pi * 2)
    else:
        return diff


def mapSteps(v: int) -> int:
    # Handle zero case
    if v == 0:
        return 0

    # Handle negative case
    sign = 1
    if v < 0:
        sign = -1
        # Invert to positive
        v = v * -1

    v = v % 3200

    # Possibly invert to negative
    return v * sign


class Control:
    node1: protocol.NodeConnection
    # node2: protocol.NodeConnection
    offset_angle_motor1: float
    offset_angle_motor2: float
    motor1: MotorContext
    motor2: MotorContext

    last_angle_motor1: float | None
    last_angle_motor2: float | None

    def __init__(
        self,
        motor1: MotorContext,
        motor2: MotorContext,
        node1_conn: protocol.NodeConnection,
        # node2_conn: protocol.NodeConnection,
    ) -> None:
        self.motor1 = motor1
        self.motor2 = motor2
        self.node1 = node1_conn
        # self.node2 = node2_conn
        self.last_angle_motor1 = None
        self.last_angle_motor2 = None

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
        self.last_angle_motor1 = None
        self.last_angle_motor2 = None

    def getSteps(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ) -> tuple[int, int]:
        motor_angle1 = ik.calc_motor_angles(
            self.motor1, coordinate, change_dir=motor1Inv
        )[0]
        motor_angle2 = ik.calc_motor_angles(
            self.motor2, coordinate, change_dir=motor2Inv
        )[0]

        motor_angle1 = motor_angle1 - self.offset_angle_motor1
        motor_angle2 = motor_angle2 - self.offset_angle_motor2

        if self.last_angle_motor1 == None or self.last_angle_motor2 == None:
            self.last_angle_motor1 = motor_angle1
            self.last_angle_motor2 = motor_angle2

        # Compute shortest angle path and set last position
        # print(motor_angle1/np.pi*180, motor_angle2/np.pi*180)
        # motor_angle1 = shortestAngle(self.last_angle_motor1, motor_angle1)
        # motor_angle2 = shortestAngle(self.last_angle_motor2, motor_angle2)
        print(motor_angle1/np.pi*180, motor_angle2/np.pi*180)
        self.last_angle_motor1 = motor_angle1
        self.last_angle_motor2 = motor_angle2

        motor1_steps = angle_to_step(motor_angle1)
        motor2_steps = angle_to_step(motor_angle2)
        return mapSteps(motor1_steps), mapSteps(motor2_steps)

    def moveTo(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ):
        steps1, steps2 = self.getSteps(coordinate, motor1Inv, motor2Inv)
        self.sendSteps(steps1, steps2)

    def sendSteps(self, steps1: int, steps2: int):
        # Because on the Node1 side, steps are subtracted by 3200 to allow negative numbers
        absolute_steps1, absolute_steps2 = steps1 + 3200, steps2 + 3200
        self.node1.debug(f"Going to pos: {steps1},{steps2}")

        message_buf = absolute_steps1.to_bytes(4, "little") + absolute_steps2.to_bytes(
            4, "little"
        )

        # Write command
        self.node1.writeMessage(message_buf)

        # Wait for done
        self.node1.readMessage()
        self.node1.debug(f"Done")
