import numpy as np
from control import Command, Move

seq1_deb = [
    # (1)
    Move(
        position=np.array([20, 65]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(delay=1),
    Move(command=Command.moveUp),
    # (2)
    Move(
        position=np.array([20, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.moveDown),
    Move(delay=1),
    Move(command=Command.moveUp),
    # (3)
    Move(
        position=np.array([20, 50]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(delay=1),
    Move(command=Command.moveUp),
    # (4)
    Move(
        position=np.array([120, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.moveDown),
    Move(delay=1),
    Move(command=Command.moveUp),
    # (5)
    Move(
        position=np.array([20, 35]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(delay=1),
    Move(command=Command.moveUp),
    # (6)
    Move(
        position=np.array([120, 50]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(command=Command.moveDown),
    Move(delay=1),
    Move(command=Command.moveUp),
]

seq1 = [
    # (1)
    Move(
        position=np.array([20, 65]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # Move(command=Command.moveUp),
    # (2)
    Move(
        position=np.array([20, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    # Move(command=Command.moveDown),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
    # (3)
    Move(
        position=np.array([20, 50]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # Move(command=Command.moveUp),
    # (4)
    Move(
        position=np.array([120, 150]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    # Move(command=Command.moveDown),
    Move(command=Command.screwIn),
    Move(command=Command.moveUp),
    # (5)
    Move(
        position=np.array([20, 35]),
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    ),
    Move(command=Command.moveDown),
    Move(command=Command.screwOut),
    # Move(command=Command.moveUp),
    # (6)
    Move(
        position=np.array([120, 50]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    # Move(command=Command.moveDown),
    Move(command=Command.screwIn),
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
