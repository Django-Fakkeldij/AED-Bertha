import ik
import time
import numpy as np

current_pos = [0, 0]

movement_array = np.array([[150,50],[140,36]])

l0 = 200 # Distance between motors , mm
l1 = 100 # mm
l2 = 100 # mm

motor_origin = np.array([0, 0])  # Origin of the motors
target_point = np.array([130, 56])  # Target position in space
    
motor = ik.MotorContext(global_origin=motor_origin, arm1_len=100, arm2_len=100)

# def move_to(x, y, stored_pos, pos_func):
#     # Get the actuated steps by comparing the desired position and current position
#     # actuated_steps = (pos_func(x, y) - stored_pos[0], pos_func(x, y)[1] - stored_pos[1])
#     actuated_steps = pos_func(x, y)
#     motor_angles = ik.calc_motor_angles()
#     # Update the current_pos by adding the actuated steps
#     stored_pos[0] += actuated_steps[0]
#     stored_pos[1] += actuated_steps[1]

#     return actuated_steps

def move_to(coordiantes_vector):
    motor_angles = ik.calc_motor_angles(motor, coordiantes_vector, change_dir=False)
    motor_steps = ik.angle_to_step(motor_angles)
    return motor_steps


def full_movement(movementarray):
    for vector in movementarray:
        move_to(vector)  
        time.sleep(1) # Adjust after determining screwing time
