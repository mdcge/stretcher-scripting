import serial
import serial.tools.list_ports as ports
import time
import sys

params = sys.argv
command = params[1]

print("Connecting to port...", end="")
ser = serial.Serial(port="COM4", baudrate=115200)
time.sleep(5)
print(" done")
print("Initializing...", end="")
ser.write(b"IDXX")
time.sleep(10)
print(" done")
print("Performing command...", end="")
ser.write(bytes(command, encoding='utf-8'))
time.sleep(3600)
print(" done")
