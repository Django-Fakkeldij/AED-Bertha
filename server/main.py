import time

import numpy as np
import protocol
from control import Control, Move
from motor import MotorContext

motor_origin1 = np.array([-27.5, 100])  # Origin of the motors
motor_origin2 = np.array([-69.5, 100])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=105, arm2_len=125)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=105, arm2_len=125)

node1 = protocol.NodeConnection("COM7", True, "Node 1")
# node2 = protocol.NodeConnection("COM6", True, "Node 2")
# control = Control(node1_conn=node1, node2_conn=node2, motor1=motor1, motor2=motor2)
control = Control(node1_conn=node1, node2_conn=None, motor1=motor1, motor2=motor2)  # type: ignore


def main():
    control.setOrigin(True, False, np.array([0, 200]))
    # control.executeMove(
    #     Move(position=np.array([0, 200]), motor1Inv=True, motor2Inv=False)
    # )

    # time.sleep(10)
    control.executeMove(
        Move(position=np.array([100, 200]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(2)
    control.executeMove(
        Move(position=np.array([100, 100]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(2)
    control.executeMove(
        Move(position=np.array([0, 200]), motor1Inv=True, motor2Inv=False)
    )


main()
