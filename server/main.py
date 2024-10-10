import time

import numpy as np
import protocol
from control import Command, Control, Move
from motor import MotorContext

motor_origin1 = np.array([70 - 145, 90])  # Origin of the motors
motor_origin2 = np.array([70 + 145, 90])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=115, arm2_len=130)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=115, arm2_len=130)

node1 = protocol.NodeConnection("COM5", True, "Node 1")
node2 = protocol.NodeConnection("COM6", True, "Node 2")
control = Control(node1_conn=node1, node2_conn=node2, motor1=motor1, motor2=motor2)


def main():
    control.setOrigin(False, False, np.array([0, 0]))
    control.executeMove(Move(position=np.array([50, 0])))
    time.sleep(2)
    control.executeMove(Move(command=Command.screwIn))
    time.sleep(2)
    control.executeMove(Move(command=Command.moveUp))
    time.sleep(2)
    control.executeMove(Move(position=np.array([0, 0])))


main()
