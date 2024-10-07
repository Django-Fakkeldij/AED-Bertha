import time

import control
import numpy as np
import protocol

from enum import Enum

node2 = protocol.NodeConnection("COM5", False, "Node 2")


class command(Enum):
    screwIn = 1111
    screwOut = 2222
    moveUp = 3333
    moveDown = 4444

m = command.screwIn.value.to_bytes(4, "little")
node2.debug(f"Sending: {m}")
node2.writeMessage(m)
node2.debug(node2.readMessage())
node2.debug(f"Done {command.moveDown.name}!")

time.sleep(1)

m = command.screwOut.value.to_bytes(4, "little")
node2.debug(f"Sending: {m}")
node2.writeMessage(m)
node2.debug(node2.readMessage())
node2.debug(f"Done {command.moveUp.name}!")
