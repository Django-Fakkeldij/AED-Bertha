import time

import control
import numpy as np
import protocol

node1 = protocol.NodeConnection("COM5", False, "Node 1")


x, y = 60, 60

steps1, steps2 = control.move_to(np.array([x, y]))

absolute_steps1, absolute_steps2 = steps1 + 3200, steps2 + 3200

node1.debug(f"Going to pos: {steps1},{steps2}")
m = absolute_steps1.to_bytes(4, "little") + absolute_steps2.to_bytes(4, "little")
node1.writeMessage(m)
node1.debug(node1.readMessage())
node1.debug(f"Done going to pos: {steps1},{steps2}!")

x, y = 0, 0

steps1, steps2 = control.move_to(np.array([x, y]))

absolute_steps1, absolute_steps2 = steps1 + 3200, steps2 + 3200

node1.debug(f"Going to pos: {steps1},{steps2}")
m = absolute_steps1.to_bytes(4, "little") + absolute_steps2.to_bytes(4, "little")
node1.writeMessage(m)
node1.debug(node1.readMessage())
node1.debug(f"Done going to pos: {steps1},{steps2}!")
