import time

from serial import Serial


class NodeConnection:
    _conn: Serial
    _debug: bool
    _name: str

    def __init__(self, port: str, debug=False, name: str = "Node") -> None:
        self._debug = debug
        self._name = name
        self._conn = Serial(port=port, baudrate=115200, timeout=0.1)
        # WARNING: MUST FIRST START WITH READING MESSAGE
        self.__debug(self.readMessage())

    def debug(self, *args):
        t = time.localtime(time.time())
        ft = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(f"{ft} | {self._name} | DEBUG |", *args)

    def debugWithoutAruidno(self, *args):
        t = time.localtime(time.time())
        ft = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(f"{ft} | {self._name} | DEBUG |", *args)

    def __debug(self, *args):
        if not self._debug:
            return
        t = time.localtime(time.time())
        ft = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(f"{ft} | {self._name} | DEBUG |", *args)

    def readMessage(self) -> bytearray:
        a = bytearray()

        # Throw away everything if it does not match start char
        length = 0
        while True:
            rb = self._conn.read()
            if rb == bytes():
                self.__debug("RECV ...")
                continue
            # mark "<" as startbyte
            if rb == b"<":
                length = int.from_bytes(self._conn.read(), "little")
                self.__debug("RECV lb: ", length)
                break
            continue

        for _ in range(length):
            rb = self._conn.read()
            a += rb

        return a

    def writeMessage(self, m: bytes):
        self._conn.write("<".encode("ascii"))
        lb = len(m).to_bytes(1, "little")
        self._conn.write(lb)
        self.__debug("SEND lb: ", int.from_bytes(lb, "little"))
        self._conn.write(m)
        self.__debug("SEND m: ", m)


# c = NodeConnection("COM5", True)
