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

home = np.array([1.3, 200 + 5])


seq1 = [
    # (1)
    Move(
        position=np.array([20, 65]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    # Move(command=Command.screwOut),
    Move(command=Command.moveUp),
    # (2)
    Move(
        position=np.array([20, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.moveDown),
    # Move(command=Command.screwIn),
    Move(command=Command.moveUp),
    # (3)
    Move(
        position=np.array([20, 50]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    # Move(command=Command.screwOut),
    Move(command=Command.moveUp),
    # (4)
    Move(
        position=np.array([120, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.moveDown),
    # Move(command=Command.screwIn),
    Move(command=Command.moveUp),
    # (5)
    Move(
        position=np.array([20, 35]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    # Move(command=Command.screwOut),
    Move(command=Command.moveUp),
    # (6)
    Move(
        position=np.array([120, 50]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.moveDown),
    # Move(command=Command.screwIn),
    Move(command=Command.moveUp),
]

seq2 = [
    # (1)
    Move(
        position=np.array([120, 50]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # (2)
    Move(
        position=np.array([20, 35]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
    # (3)
    Move(
        position=np.array([120, 150]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # (4)
    Move(
        position=np.array([20, 50]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
    # (5)
    Move(
        position=np.array([20, 150]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # (6)
    Move(
        position=np.array([20, 65]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
]

sub_seq1 = [
    # (1)
    Move(
        position=np.array([20, 65]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # (2)
    Move(
        position=np.array([20, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
]
sub_seq2 = [
    # (5)
    Move(
        position=np.array([20, 150]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # (6)
    Move(
        position=np.array([20, 65]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
]


def main():
    control.setOrigin(True, False, home)

    t1 = time.time()

    for move in seq1:
        control.executeMove(move)
        input("next:")

    t2 = time.time()

    print("TOTAL SEQUENCE TIME: ", t2 - t1, " seconds")

    # for move in seq2:
    #     control.executeMove(move)

    # (HOME)
    # input("Enter for next: ")
    control.executeMove(
        Move(
            position=np.array([70, 200]),
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        )
    )
    control.executeMove(
        Move(position=home, motor1Inv=True, motor2Inv=False, command=Command.moveUp)
    )


main()
