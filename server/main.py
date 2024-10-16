import time

import numpy as np
import protocol
from control import Control, Move
from motor import MotorContext

motor_origin1 = np.array([-27.5, 100])  # Origin of the motors
motor_origin2 = np.array([-69.5, 100])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=105, arm2_len=125)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=105, arm2_len=125)

node1 = protocol.NodeConnection("COM8", True, "Node 1")
# node2 = protocol.NodeConnection("COM6", True, "Node 2")
# control = Control(node1_conn=node1, node2_conn=node2, motor1=motor1, motor2=motor2)
control = Control(node1_conn=node1, node2_conn=None, motor1=motor1, motor2=motor2)  # type: ignore

interval = 2


def main():
    control.setOrigin(True, False, np.array([2.15, 200 + 7 - (3.7 / 2)]))

    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([20, 65]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([20, 150]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([20, 50]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([120, 150]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([20, 35]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([120, 50]), motor1Inv=True, motor2Inv=False)
    )
    time.sleep(interval)
    control.executeMove(
        Move(position=np.array([3, 205]), motor1Inv=True, motor2Inv=False)
    )


def main2():
    t = 0
    control.setOrigin(True, False, np.array([2.15, 200 + 7 - (3.7 / 2)]))

    while True:
        t += 0.01
        time.sleep(interval)
        control.executeMove(
            Move(
                position=np.array([70 + np.cos(t) * 30, 100 + np.sin(t) * 30]),
                motor1Inv=True,
                motor2Inv=False,
            )
        )


main()
