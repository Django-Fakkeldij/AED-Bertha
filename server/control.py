import time

import ik
import numpy as np

current_pos = [0, 0]

movement_array = np.array([[150, 50], [140, 36]])


motor_origin1 = np.array([70 - 145, 90])  # Origin of the motors
motor_origin2 = np.array([70 + 145, 90])  # Origin of the motors
# target_point = np.array([130, 56])  # Target position in space

motor1 = ik.MotorContext(global_origin=motor_origin1, arm1_len=115, arm2_len=130)
motor2 = ik.MotorContext(global_origin=motor_origin2, arm1_len=115, arm2_len=130)

# def move_to(x, y, stored_pos, pos_func):
#     # Get the actuated steps by comparing the desired position and current position
#     # actuated_steps = (pos_func(x, y) - stored_pos[0], pos_func(x, y)[1] - stored_pos[1])
#     actuated_steps = pos_func(x, y)
#     motor_angles = ik.calc_motor_angles()
#     # Update the current_pos by adding the actuated steps
#     stored_pos[0] += actuated_steps[0]
#     stored_pos[1] += actuated_steps[1]

#     return actuated_steps


def move_to(coordiantes_vector) -> tuple[int, int]:
    motor_angles1 = ik.calc_motor_angles(motor1, coordiantes_vector, change_dir=False)
    motor_angles2 = ik.calc_motor_angles(motor2, coordiantes_vector, change_dir=False)
    motor_steps = ik.angle_to_step([motor_angles1[0], motor_angles2[0]])
    return motor_steps


def full_movement(movementarray):
    for vector in movementarray:
        move_to(vector)
        # time.sleep(1)  # Adjust after determining screwing time
