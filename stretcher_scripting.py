import numpy as np
import serial
import time

# ser = serial.Serial(
#     port="COM4",
#     baudrate=115200,
#     parity=serial.PARITY_ODD,
#     stopbits=serial.STOPBITS_TWO,
#     bytesize=serial.SEVENBITS
# )

while True:
    print("M155")
    time.sleep(5)
