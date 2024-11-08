import serial
import sys

params = sys.argv
command = params[1]

with serial.Serial as ser:
    port = "COM4"
    baudrate = 115200
    ser.open()
    ser.write(command)
