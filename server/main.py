import time

import control
import numpy as np
import protocol

node1 = protocol.NodeConnection("COM5", False, "Node 1")

movement_array = np.array([[150, 50], [140, 36]])


motor_origin1 = np.array([70 - 145, 90])  # Origin of the motors
motor_origin2 = np.array([70 + 145, 90])  # Origin of the motors

motor1 = control.MotorContext(global_origin=motor_origin1, arm1_len=115, arm2_len=130)
motor2 = control.MotorContext(global_origin=motor_origin2, arm1_len=115, arm2_len=130)
