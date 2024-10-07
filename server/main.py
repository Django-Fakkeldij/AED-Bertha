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
motor1Inv = True
motor2Inv = False

for i in range(0, 3200 * 10, 800):
    controller.sendSteps(i, i)

# controller.setOrigin(motor1Inv=motor1Inv, motor2Inv=motor2Inv)
# controller.setOrigin(
#     motor1Inv=motor1Inv, motor2Inv=motor2Inv, offset=np.array([15, 45])
# )
# controller.moveTo(np.array([50, 20]), motor1Inv=motor1Inv, motor2Inv=motor2Inv)
# time.sleep(2)
# controller.moveTo(np.array([50, 180]), motor1Inv=motor1Inv, motor2Inv=motor2Inv)
