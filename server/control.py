import ik
import numpy as np
import protocol
import time
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


class Control:
    node1: protocol.NodeConnection
    # node2: protocol.NodeConnection
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
        # node2_conn: protocol.NodeConnection,
    ) -> None:
        self.motor1 = motor1
        self.motor2 = motor2
        self.node1 = node1_conn
        # self.node2 = node2_conn
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
        # For setting last step in proper pos
        self.moveToDirect(
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

        motor1_steps = angle_to_step(motor_angle1)
        motor2_steps = angle_to_step(motor_angle2)

        mapped_steps1 = mapSteps(motor1_steps, self.last_steps_motor1)
        mapped_steps2 = mapSteps(motor2_steps, self.last_steps_motor2)

        self.last_steps_motor1 = mapped_steps1
        self.last_steps_motor2 = mapped_steps2

        mapped_steps1_absolute = mapped_steps1 - angle_to_step(self.offset_angle_motor1)
        mapped_steps2_absolute = mapped_steps2 - angle_to_step(self.offset_angle_motor2)

        return mapped_steps1_absolute, mapped_steps2_absolute

    def moveToDirect(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ):
        steps1, steps2 = self.getSteps(coordinate, motor1Inv, motor2Inv)
        self.sendStepsDebug(steps1, steps2) #Replace with sendSteps() when using Arduino
        self.last_position = coordinate

    def moveTo(
        self, coordinate: np.ndarray, motor1Inv: bool = False, motor2Inv: bool = False
    ):
        self.moveToInterpolate(
            self.last_position, coordinate, motor1Inv=motor1Inv, motor2Inv=motor2Inv
        )

    def moveToInterpolate(
        self,
        coordinate1: np.ndarray,
        coordinate2: np.ndarray,
        motor1Inv: bool = False,
        motor2Inv: bool = False,
    ):
        diff_vec = coordinate2 - coordinate1
        steps = int(np.sqrt(diff_vec[0] ** 2 + diff_vec[1] ** 2))
        # steps = 200
        for i in range(round(steps)):
            abs_pos = coordinate1 + (i * (diff_vec / steps))
            self.moveToDirect(abs_pos, motor1Inv=motor1Inv, motor2Inv=motor2Inv)

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

    def sendStepsDebug(self, steps1: int, steps2: int):
        absolute_steps1, absolute_steps2 = steps1 + 3200, steps2 + 3200
        print(f"Going to pos: {steps1},{steps2}")


# motor_origin1 = np.array([70 - 145, 90])  # Origin of the motors
# motor_origin2 = np.array([70 + 145, 90])  # Origin of the motors

# motor1 = MotorContext(global_origin=motor_origin1, arm1_len=115, arm2_len=130)
# motor2 = MotorContext(global_origin=motor_origin2, arm1_len=115, arm2_len=130)


# controller = Control(motor1, motor2, None)
# Min = False
# Plus = True


# controller.setOrigin(
#     motor1Inv=Min, motor2Inv=Min, offset=np.array([0, 0])
# )
# controller.moveTo(np.array([50, 0]))
# time.sleep(2)
# controller.moveTo(np.array([50, 50]))
# time.sleep(2)
# controller.moveTo(np.array([0, 50]))
# time.sleep(2)
# controller.moveTo(np.array([20, 150]))
# time.sleep(2)