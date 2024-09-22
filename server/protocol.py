import time
from enum import Enum

import serial


def debug(*args):
    print("DEBUG |", *args)


conn = serial.Serial(port="COM4", baudrate=115200, timeout=None)


def readMessage() -> bytearray:
    a = bytearray()

    # Throw away everything if it does not match start char
    while True:
        rb = conn.read()
        if rb == b"<":
            break
        continue

    while True:
        rb = conn.read()
        if rb != b">":
            a += rb
        else:
            break

    return a


def writeMessage(m: bytes):
    conn.write(b"<")
    conn.write(m)
    conn.write(b">")


debug(readMessage().decode("ascii"))
writeMessage("ping".encode("ascii"))
debug(readMessage().decode("ascii"))
