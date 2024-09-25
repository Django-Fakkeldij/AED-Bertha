import numpy as np


class MotorContext:
    def __init__(self, global_origin: np.ndarray, arm1_len: float, arm2_len: float):
        self.global_origin = global_origin
        self.arm1_len = arm1_len
        self.arm2_len = arm2_len
