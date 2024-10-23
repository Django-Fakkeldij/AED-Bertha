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
# control = Control(node1_conn=node1, node2_conn=None, motor1=motor1, motor2=motor2)  # type: ignore
control = Control(node1_conn=node1, node2_conn=node2, motor1=motor1, motor2=motor2)

interval = 4

home = np.array([1.35, 205.2])
mid = np.array([70, 100])


def main(forward=True, backward=True, homing=False, benchmark=True):

    if benchmark:
        control.benchmark()

    if homing:
        startHoming()

    t1 = time.time()

    control.setOrigin(True, False, home)
    control.executeMove(moveTo(mid))
    if forward:
        for move in seq1:
            # input("(FORWARD) ->")
            control.executeMove(move)

    control.executeMove(moveTo(mid))

    t2 = time.time()
    print("TOTAL SEQUENCE TIME: ", t2 - t1, " seconds")

    if backward:
        for move in seq2:
            # input("(REV) ->")
            control.executeMove(move)

    input("(HOME) ->")

    # (HOME)
    for move in goToHome(home):
        control.executeMove(move)


def scanning(origin: np.ndarray, pos: np.ndarray):
    scan = input("Start scan seq? (y)   ")
    if scan.strip() == "y":
        new_origin = np.array([origin[0], origin[1]])
        while True:
            incr_x = float(input(f"(incr. X) {new_origin[0]} + : "))
            incr_y = float(input(f"(incr. Y) {new_origin[1]} + : "))

            new_origin[0] = new_origin[0] + incr_x
            new_origin[1] = new_origin[1] + incr_y

            print(
                f"Home defined as:\n\tabsolute: [{0 + new_origin[0]}, {new_origin[1]}]",
            )
            control.setOrigin(True, False, offset=new_origin, doNotMove=True)
            control.moveTo(pos, motor1Inv=True, motor2Inv=False)
            q = input("Quit? (q):   ")
            if q.strip() == "q":
                break


def startHoming():
    control.setOrigin(True, False, home)

    x_offset = 0
    y_offset = 0
    while True:
        low = input("lower? (y) ")
        if low.strip() == "y":
            control.executeMove(
                Move(command=Command.moveDown),
            )
            input("Continue?...")
            control.executeMove(
                Move(command=Command.moveUp),
            )
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
        scanning(
            origin=np.array([0 + x_offset, 200 + y_offset]), pos=np.array([120, 50])
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
        scanning(
            origin=np.array([0 + x_offset, 200 + y_offset]), pos=np.array([120, 150])
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
        scanning(
            origin=np.array([0 + x_offset, 200 + y_offset]), pos=np.array([20, 150])
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
        scanning(
            origin=np.array([0 + x_offset, 200 + y_offset]), pos=np.array([20, 35])
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


main()
