import math

import numpy as np
from motor import MotorContext


def solve_cosine_rule(target_vec_len: float, arm1_len: float, arm2_len: float):
    cos_value1 = (target_vec_len**2 + arm1_len**2 - arm2_len**2) / (
        2 * target_vec_len * arm1_len
    )
    cos_value2 = (arm2_len**2 + arm1_len**2 - target_vec_len**2) / (
        2 * arm2_len * arm1_len
    )

    cos_value1 = np.clip(cos_value1, -1, 1)
    cos_value2 = np.clip(cos_value2, -1, 1)

    arm1_angle = math.acos(cos_value1)
    arm2_angle = math.acos(cos_value2)

    return [arm1_angle, arm2_angle]


# Function to rotate a 2D vector by an angle
def rotate_vector(vec, angle: float):
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    return np.dot(rotation_matrix, vec)


def calc_motor_angles(
    motor: MotorContext, target: np.ndarray, change_dir: bool = False
) -> tuple[float, float]:

    local_target = target - motor.global_origin
    local_angle = math.atan2(local_target[1], local_target[0])  # Get angle to target
    local_len = np.linalg.norm(local_target)

    arm1_angle, _ = solve_cosine_rule(local_len, motor.arm1_len, motor.arm2_len)  # type: ignore

    if change_dir:
        arm1_real_angle = -arm1_angle + local_angle
    else:
        arm1_real_angle = arm1_angle + local_angle

    arm1 = np.array([motor.arm1_len, 0])
    arm1_rotated = rotate_vector(arm1, arm1_real_angle)

    arm1_to_target = target - (motor.global_origin + arm1_rotated)
    real_arm2_angle = math.atan2(arm1_to_target[1], arm1_to_target[0])

    return arm1_real_angle, real_arm2_angle
