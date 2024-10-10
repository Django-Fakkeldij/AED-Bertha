import time

import control
import numpy as np
import protocol
from motor import MotorContext

node1 = protocol.NodeConnection("COM5", True, "Node 1")


motor_origin1 = np.array([70 - 145, 90])  # Origin of the motors
motor_origin2 = np.array([70 + 145, 90])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=115, arm2_len=130)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=115, arm2_len=130)


controller = control.Control(motor1, motor2, node1, None)  # type: ignore
Min = False
Plus = True

motor1_conf = Min
motor2_conf = Min

controller.setOrigin(
    motor1Inv=motor1_conf, motor2Inv=motor2_conf, offset=np.array([0, 0])
)
controller.moveTo(np.array([0, 0]), motor1Inv=motor1_conf, motor2Inv=motor2_conf)
controller.moveTo(np.array([140, 0]), motor1Inv=motor1_conf, motor2Inv=motor2_conf)
# controller.moveTo(np.array([140, 210]), motor1Inv=motor1_conf, motor2Inv=motor2_conf)
# time.sleep(2)
# controller.moveTo(np.array([50, 50]), motor1Inv=motor1_conf, motor2Inv=motor2_conf)
