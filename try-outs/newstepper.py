import time
from pyfirmata import Arduino, util

# Define the pins used on the CNC shield
X_STEP_PIN = 2
X_DIR_PIN = 5
Y_STEP_PIN = 3
Y_DIR_PIN = 6
Z_STEP_PIN = 4
Z_DIR_PIN = 7
ENABLE_PIN = 8

STEP_DELAY = 0.000001

# Initialize the Arduino board using pyfirmata
board = Arduino('COM5')  # Replace 'COM3' with your port (Linux: '/dev/ttyUSB0')

# Enable the stepper motor (ENABLE_PIN = LOW)
board.digital[ENABLE_PIN].write(0)  # LOW to enable the motor

xstepper = board.digital[X_STEP_PIN]
xstepper_dir = board.digital[X_DIR_PIN]

ystepper = board.digital[Y_STEP_PIN]
ystepper_dir = board.digital[Y_DIR_PIN]

zstepper = board.digital[Z_STEP_PIN]
zstepper_dir = board.digital[Z_DIR_PIN]

# def step_direction(step_input, stepper_motor):
#     if step_input < 0:
#         stepper_motor.write(0)
#     else:
#         stepper_motor.write(1)

def step_motor(steps):
    xsteps, ysteps, zsteps = steps

    # step_direction(xsteps, xstepper_dir)
    # step_direction(ysteps, ystepper_dir)
    # step_direction(zsteps, zstepper_dir)

    xstepper_dir.write(1 if xsteps > 0 else 0)  # HIGH for forward, LOW for backward on X-axis
    ystepper_dir.write(1 if ysteps > 0 else 0)  # HIGH for forward, LOW for backward on Y-axis
    zstepper_dir.write(1 if zsteps > 0 else 0)  # HIGH for forward, LOW for backward on Z-axis


    xsteps = abs(xsteps)
    ysteps = abs(ysteps)
    zsteps = abs(zsteps)

    # Step the motor
    for _ in range(xsteps):
        xstepper.write(1)  # HIGH to step
        time.sleep(STEP_DELAY)  # Delay for step timing
        xstepper.write(0)  # LOW to finish the step
        time.sleep(STEP_DELAY)  # Adjust speed with the delay

    # for _ in range(abs(ysteps)):
    #     ystepper.write(1)  # HIGH to step
    #     time.sleep(STEP_DELAY)  # Delay for step timing
    #     ystepper.write(0)  # LOW to finish the step
    #     time.sleep(STEP_DELAY)  # Adjust speed with the delay



    # for _ in range(max(xsteps, ysteps, zsteps)):
    #     # Step the X motor if there are steps remaining
    #     if xsteps > 0:
    #         xstepper.write(1)  # HIGH to step X motor
    #     if ysteps > 0:
    #         ystepper.write(1)  # HIGH to step Y motor
    #     if zsteps > 0:
    #         zstepper.write(1)  # HIGH to step Z motor

    #     time.sleep(STEP_DELAY)  # Control the speed of the steps

    #     xstepper.write(0)  # LOW to finish X motor step
    #     ystepper.write(0)  # LOW to finish Y motor step
    #     zstepper.write(0)  # LOW to finish Z motor step

    #     time.sleep(STEP_DELAY)  # Adjust speed with the delay

    #     # Decrease step counts for each motor
    #     if xsteps > 0:
    #         xsteps -= 1
    #     if ysteps > 0:
    #         ysteps -= 1
    #     if zsteps > 0:
    #         zsteps -= 1

try:
    while True:
        # # Get user input for motor direction
        direction = input("Enter 'f' to move forward, 'b' to move backward, or 'q' to quit: ")

        if direction == 'f':
            print("Forward 3200 steps")
            step_motor([3200, 800, 0])
        elif direction == 'b':
            print("Backward 3200 steps")
            step_motor([-3200, -800, 0])
        elif direction == 'q':
            break
        else:
            print("Invalid input, please enter 'f', 'b', or 'q'.")

# Get user input for X and Y steps as an array
        # steps_input = input("Enter the steps as an array ([num,num,num]), or 'q' to quit: ")
        # # Convert the input string to a list of integers
        # if steps_input == 'q':
        #     break

        # steps = [int(s) for s in steps_input.strip('[]').split(',')]

        # x_steps, y_steps, z_steps = steps

        # if x_steps != 0 or y_steps != 0 or z_steps != 0:
        #     print(f"Moving X by {x_steps} steps and Y by {y_steps} steps and Z by {z_steps} steps")
        #     step_motor(steps)
        # else:
        #     print("No movement requested, please enter a non-zero number of steps.")
finally:
    # Disable the motor when done
    board.digital[ENABLE_PIN].write(1)  # HIGH to disable the motor
    board.exit()  # Clean up connection with the Arduino
