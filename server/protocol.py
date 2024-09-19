import time
from enum import Enum

import serial


class Command(Enum):
    Stop = 0
    Start = 1
    RotateMotor1 = 2
    RotateMotor2 = 3


conn = serial.Serial(port="COM4", baudrate=115200, timeout=0.5)


def writeCommand(command: Command, args: bytes):
    args_len = len(args)

    start_byte = 0b10101010

    arr = (
        start_byte.to_bytes(1, "big")
        + start_byte.to_bytes(1, "big")
        + command.value.to_bytes(1, "big")
        + args_len.to_bytes(1, "big")
        + args
    )

    if len(arr) > 64:
        raise Exception("Message to big to fit in client buffer")

    print("SERVER | ", arr, " | LEN: ", len(arr))

    for i in range(len(arr)):
        conn.write(arr[i : i + 1])
        time.sleep(0.1)

    print("SERVER | ", "Done sending")
    a = str()
    while True:
        a += conn.read().decode()
        print("CLIENT | ", a)


writeCommand(Command.Start, b"start123")
