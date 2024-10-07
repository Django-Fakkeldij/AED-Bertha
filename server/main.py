import time

import control
import numpy as np
import protocol
from motor import MotorContext

node1 = protocol.NodeConnection("COM4", True, "Node 1")

movement_array = np.array([[150, 50], [140, 36]])


motor_origin1 = np.array([70 - 145, 90])  # Origin of the motors
motor_origin2 = np.array([70 + 145, 90])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=115, arm2_len=130)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=115, arm2_len=130)


controller = control.Control(motor1, motor2, node1)
Min = False
Plus = True

controller.setOrigin(
    motor1Inv=Min, motor2Inv=Plus, offset=np.array([15, 45])
)
controller.moveTo(np.array([50, 20]))
time.sleep(2)
controller.moveTo(np.array([50, 180]))
