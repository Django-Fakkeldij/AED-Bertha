import time
from enum import Enum

import serial


def debug(*args):
    print("DEBUG |", *args)


conn = serial.Serial(port="COM4", baudrate=115200, timeout=2)


def readMessage() -> bytearray:
    a = bytearray()

    # Throw away everything if it does not match start char
    length = 0
    while True:
        rb = conn.read()
        if rb == bytes():
            debug("...")
            continue
        # mark "<" as startbyte
        if rb == b"<":
            debug("got start byte")
            length = int.from_bytes(conn.read(), "little")
            debug("got length byte: ", length)
            break
        continue

    for _ in range(length):
        rb = conn.read()
        a += rb

    return a


def writeMessage(m: bytes):
    conn.write("<".encode("ascii"))
    lb = len(m).to_bytes(1, "little")
    conn.write(lb)
    debug("lb: ", int.from_bytes(lb, "little"))
    conn.write(m)


debug("Starting")
debug(readMessage().decode("ascii"))
writeMessage("ping".encode("ascii"))
debug(readMessage().decode("ascii"))
