import time

import serial

arduino = serial.Serial(port="COM5", baudrate=115200, timeout=0.1)


# def write_read(x):
#     print("sending: ", x, "...")
#     arduino.write(bytes(x, "utf-8"))
#     time.sleep(2)
#     print("sending done")

#     d = arduino.read_until(b"DONE").decode()
#     print(d)
#     return d

def write_read(x):
    print("sending: ", x, "...")
    arduino.write(bytes(x, "utf-8"))
    time.sleep(2)

    while True:
        # Read until "DONE" is received or timeout occurs
        d = arduino.read_until(b"DONE").decode()
        if "DONE" in d:
            print("Arduino response: ", d)
            break  # Exit the loop once "DONE" is received

    print("sending done")
    return d


# i1, i2 = 200, 200

# while True:
#     i1, i2 = i1 + 100, i2 + 100
#     value = write_read(f"{i1},{i2}")
