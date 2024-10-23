import time

import numpy as np
import protocol
from control import Command, Control, Move
from motor import MotorContext
from sequences import *

motor_origin1 = np.array([-27.5, 100])  # Origin of the motors
motor_origin2 = np.array([-69.5, 100])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=105, arm2_len=125)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=105, arm2_len=125)

node1 = protocol.NodeConnection("COM8", False, "Node 1")
node2 = protocol.NodeConnection("COM6", False, "Node 2")
control = Control(node1_conn=node1, node2_conn=node2, motor1=motor1, motor2=motor2)

interval = 4

home = np.array([0, 200]) + np.array([0.65, 4.9])
mid = np.array([70, 100])


def main(forward=True, backward=True):

    t1 = time.time()

    control.setOrigin(True, False, home)
    control.executeMove(moveTo(mid))
    if forward:
        for move in seq1:
            control.executeMove(move)

    control.executeMove(moveTo(mid))

    t2 = time.time()
    print("TOTAL SEQUENCE TIME: ", t2 - t1, " seconds")
    time.sleep(5)

    if backward:
        for move in seq2:
            control.executeMove(move)

    # (HOME)
    for move in goToHome(home):
        control.executeMove(move)


def startHoming():
    control.setOrigin(True, False, home)

    x_offset = 0
    y_offset = 0
    while True:
        y = input("Enter new? (y)   ")
        if y.strip() == "y":
            x_offset = float(input("origin:  x + 0 + ").strip())
            y_offset = float(input("origin: y + 200 + ").strip())
        print(
            f"Home defined as:\n\trelative: [{x_offset}, {y_offset}]\n\tabsolute: [{0 + x_offset}, {200 + y_offset}]",
        )
        control.executeMove(
            Move(command=Command.moveUp),
        )
        control.setOrigin(True, False, np.array([0 + x_offset, 200 + y_offset]))
        input("Enter to move to target 1...   ")
        control.executeMove(
            Move(
                position=np.array([120, 50]),
                motor1Inv=True,
                motor2Inv=False,
            ),
        )
        control.executeMove(
            Move(command=Command.moveDown),
        )
        input("Enter to move to target 2...   ")
        control.executeMove(
            Move(command=Command.moveUp),
        )
        control.executeMove(
            Move(
                position=np.array([120, 150]),
                motor1Inv=True,
                motor2Inv=False,
            ),
        )
        control.executeMove(
            Move(command=Command.moveDown),
        )
        input("Enter to move to target 3...   ")
        control.executeMove(
            Move(command=Command.moveUp),
        )
        control.executeMove(
            Move(
                position=np.array([20, 150]),
                motor1Inv=True,
                motor2Inv=False,
            ),
        )
        control.executeMove(
            Move(command=Command.moveDown),
        )
        input("Enter to move to target 4...   ")
        control.executeMove(
            Move(command=Command.moveUp),
        )
        control.executeMove(
            Move(
                position=np.array([20, 35]),
                motor1Inv=True,
                motor2Inv=False,
            ),
        )
        control.executeMove(
            Move(command=Command.moveDown),
        )
        q = input("Quit? (enter 'q')    ")
        control.executeMove(
            Move(command=Command.moveUp),
        )

        control.executeMove(
            Move(
                position=np.array([70, 200]),
                motor1Inv=True,
                motor2Inv=False,
            ),
        )
        control.setOrigin(True, False, np.array([0 + x_offset, 200 + y_offset]))
        if q.strip() == "q":
            break


# startHoming()
main(forward=True)
