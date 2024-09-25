import ik
import numpy as np
import protocol
from motor import MotorContext


def angle_to_step(angle):
    steps_per_rotation = 3200
    steps = round(angle / (2 * np.pi) * steps_per_rotation)
    return steps


class Control:
    node1: protocol.NodeConnection
    # node2: protocol.NodeConnection
    offset_angle_motor1: float
    offset_angle_motor2: float
    motor1: MotorContext
    motor2: MotorContext

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

    def setOrigin(self, motor1Inv: bool = False, motor2Inv: bool = False):
        # Sets offsets
        self.offset_angle_motor1 = ik.calc_motor_angles(
            self.motor1, np.array([0, 0]), change_dir=motor1Inv
        )[0]
        self.offset_angle_motor2 = ik.calc_motor_angles(
            self.motor2, np.array([0, 0]), change_dir=motor2Inv
        )[0]

    def getSteps(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ) -> tuple[int, int]:
        motor_angles1 = ik.calc_motor_angles(
            self.motor1, coordinate, change_dir=motor1Inv
        )
        motor_angles2 = ik.calc_motor_angles(
            self.motor2, coordinate, change_dir=motor2Inv
        )
        motor1_steps = angle_to_step(motor_angles1[0] + self.offset_angle_motor1)
        motor2_steps = angle_to_step(motor_angles2[0] + self.offset_angle_motor2)
        return motor1_steps, motor2_steps

    def moveTo(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ):
        steps1, steps2 = self.getSteps(coordinate)
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
