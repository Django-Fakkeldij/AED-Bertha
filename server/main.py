import time

import numpy as np
import protocol
from control import Command, Control, Move
from motor import MotorContext

motor_origin1 = np.array([-27.5, 100])  # Origin of the motors
motor_origin2 = np.array([-69.5, 100])  # Origin of the motors

motor1 = MotorContext(global_origin=motor_origin1, arm1_len=105, arm2_len=125)
motor2 = MotorContext(global_origin=motor_origin2, arm1_len=105, arm2_len=125)

node1 = protocol.NodeConnection("COM8", False, "Node 1")
node2 = protocol.NodeConnection("COM6", False, "Node 2")
control = Control(node1_conn=node1, node2_conn=node2, motor1=motor1, motor2=motor2)

interval = 4

home = np.array([0.1, 200 + 3.9])


def main():
    control.setOrigin(True, False, home)

    # Screw 1
    input("Enter for next: ")
    control.executeMove(Move(command=Command.screwIn))
    input("Enter for next: ")
    control.executeMove(Move(command=Command.screwOut))
    input("Enter for next: ")
    control.executeMove(
        Move(
            position=home,
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        )
    )
    input("Enter for next: ")
    control.executeMove(
        Move(
            position=np.array([20, 35]),
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        )
    )
    input("Enter for next: ")
    control.executeMove(Move(command=Command.moveDown))
    input("Enter for next: ")
    control.executeMove(Move(command=Command.moveUp))

    input("Enter for next: ")
    control.executeMove(
        Move(
            position=home,
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        )
    )

    # control.executeMove(
    #     Move(
    #         position=np.array([20, 65]),
    #         motor1Inv=True,
    #         motor2Inv=False,
    #         command=Command.moveDown,
    #     )
    # )
    # input("Enter for next: ")
    # control.executeMove(
    #     Move(
    #         position=np.array([20, 50]),
    #         motor1Inv=True,
    #         motor2Inv=False,
    #         command=Command.moveDown,
    #     )
    # )
    # input("Enter for next: ")
    # control.executeMove(
    #     Move(
    #         position=np.array([20, 150]),
    #         motor1Inv=True,
    #         motor2Inv=False,
    #         command=Command.moveDown,
    #     )
    # )
    # input("Enter for next: ")
    # control.executeMove(
    #     Move(
    #         position=np.array([120, 150]),
    #         motor1Inv=True,
    #         motor2Inv=False,
    #         command=Command.moveDown,
    #     )
    # )
    # input("Enter for next: ")
    # control.executeMove(
    #     Move(
    #         position=np.array([120, 50]),
    #         motor1Inv=True,
    #         motor2Inv=False,
    #         command=Command.moveDown,
    #     )
    # )
    # input("Enter for next: ")
    # control.executeMove(
    #     Move(
    #         position=home,
    #         motor1Inv=True,
    #         motor2Inv=False,
    #         command=Command.moveDown,
    #     )
    # )


def main2():
    t = 0
    control.setOrigin(True, False, home)

    control.executeMove(Move(command=Command.moveDown))


main()
