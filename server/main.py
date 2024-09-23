import time

import protocol

node1 = protocol.NodeConnection("COM5", False, "Node 1")

t1 = 0
t2 = 3200
while True:
    node1.debug(f"Going to pos: {t1},{t2}")
    m = t1.to_bytes(4, "little") + t2.to_bytes(4, "little")
    node1.writeMessage(m)
    node1.debug(node1.readMessage())
    t1 += 400
    t2 += 400
