import serial
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Port name", type=str)
parser.add_argument("-c", "--command", help="Stretcher command", type=str)
parser.add_argument("-br", "--baud-rate", help="Baud rate of the connection", type=int, default=115200)
args = parser.parse_args()
print(args)

print("Connecting to port...", end="")
ser = serial.Serial(port=args.port, baudrate=args.baud_rate)
time.sleep(5)
print(" done")
print("Initializing...", end="")
ser.write(b"IDXX")
time.sleep(10)
print(" done")
print("Performing command...", end="")
ser.write(bytes(args.command, encoding='utf-8'))
time.sleep(3600)
print(" done")
