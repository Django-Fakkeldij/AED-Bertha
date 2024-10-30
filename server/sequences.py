import numpy as np
from control import Command, Move


def screwInMoves(position: np.ndarray) -> tuple[Move, Move, Move]:
    return (
        Move(
            position=position, motor1Inv=True, motor2Inv=False, command=Command.moveUp
        ),
        # Move(command=Command.moveDown),
        Move(command=Command.screwIn),
        Move(command=Command.moveUp),
    )


def screwInMovesDebug(position: np.ndarray) -> tuple[Move, Move, Move, Move]:
    return (
        Move(
            position=position, motor1Inv=True, motor2Inv=False, command=Command.moveUp
        ),
        Move(command=Command.moveDown),
        Move(delay=1),
        Move(command=Command.moveUp),
    )


def screwOutMoves(position: np.ndarray) -> tuple[Move, Move, Move]:
    return (
        Move(
            position=position,
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        ),
        Move(command=Command.moveDown),
        Move(command=Command.screwOut),
    )


def screwOutMovesDebug(position: np.ndarray) -> tuple[Move, Move, Move, Move]:
    return (
        Move(
            position=position,
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        ),
        Move(command=Command.moveDown),
        Move(delay=1),
        Move(command=Command.moveUp),
        # Move(command=Command.screwOut),
    )


def goToHome(home: np.ndarray) -> tuple[Move, Move]:
    return (
        Move(
            position=np.array([70, 200]),
            motor1Inv=True,
            motor2Inv=False,
            command=Command.moveUp,
        ),
        Move(position=home, motor1Inv=True, motor2Inv=False, command=Command.moveUp),
    )


def moveTo(mid: np.ndarray) -> Move:
    return Move(
        position=mid,
        motor1Inv=True,
        motor2Inv=False,
        command=Command.moveUp,
    )


trace_lines = [
    Move(command=Command.moveDown),
    Move(
        position=np.array([5, 200]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(
        position=np.array([140, 200]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(
        position=np.array([140, 0]),
        motor1Inv=True,
        motor2Inv=False,
    ),
    Move(
        position=np.array([5, 0]),
        motor1Inv=True,
        motor2Inv=False,
    ),
]

seq1_deb = [
    # (1)
    *screwOutMovesDebug(np.array([20, 65])),
    # (2)
    *screwInMovesDebug(np.array([20, 150])),
    # (3)
    *screwOutMovesDebug(np.array([20, 50])),
    # (4)
    *screwInMovesDebug(np.array([120, 150])),
    # (5)
    *screwOutMovesDebug(np.array([20, 35])),
    # (6)
    *screwInMovesDebug(np.array([120, 50])),
]

seq1 = [
    # (1)
    *screwOutMoves(np.array([20, 65])),
    # (2)
    *screwInMoves(np.array([20, 150])),
    # (3)
    *screwOutMoves(np.array([20, 50])),
    # (4)
    *screwInMoves(np.array([120, 150])),
    # (5)
    *screwOutMoves(np.array([20, 35])),
    # (6)
    *screwInMoves(np.array([120, 50])),
]

seq2 = [
    # (1)
    *screwOutMoves(np.array([120, 50])),
    # (2)
    *screwInMoves(np.array([20, 35])),
    # (3)
    *screwOutMoves(np.array([120, 150])),
    # (4)
    *screwInMoves(np.array([20, 50])),
    # (5)
    *screwOutMoves(np.array([20, 150])),
    # (6)
    *screwInMoves(np.array([20, 65])),
]

sub_seq1 = [
    # (1)
    *screwOutMoves(np.array([20, 65])),
    # (2)
    *screwInMoves(np.array([20, 150])),
]
sub_seq2 = [
    # (5)
    *screwOutMoves(np.array([20, 150])),
    # (6)
    *screwInMoves(np.array([20, 65])),
]
