import numpy as np
import matplotlib.pyplot as plt

l0 = 200 # distance between motors
l1 = 100 # mm
l2 = 100 # mm


def motor_angle(x, y):
    alpha1 = np.arccos((l1**2 + ((l0 + x)**2 + y**2) - l2**2) / (2 * l1 * np.sqrt((l0 + x)**2 + y**2)))

    # Calculate alpha2
    alpha2 = np.arccos((l1**2 + ((l0 - x)**2 + y**2) - l2**2) / (2 * l1 * np.sqrt((l0 - x)**2 + y**2)))

    # Calculate beta1
    beta1 = np.arctan(y / (l0 + x))

    # Calculate beta2
    beta2 = np.arctan(y / (l0 - x))

    theta1 = beta1 + alpha1
    theta2 = np.pi-beta2+alpha2

    return theta1, theta2

def angle_to_step(angle_func):
    xsteps = angle_func[0] / (2 * np.pi) * 3200
    ysteps = angle_func[1] / (2 * np.pi) * 3200
    return xsteps, ysteps

