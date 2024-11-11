import serial
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Port name", type=str)
parser.add_argument("-br", "--baud-rate", help="Baud rate of the connection", type=int, default=115200)
parser.add_argument("-f", "--force", help="Force to set the stretcher to", type=float)
parser.add_argument("-dp", "--data-points", help="Number of times to measure the force", type=int)
parser.add_argument("-s", "--sleep-time", help="Time between measurements", dtype=int)
args = parser.parse_args()

print("Connecting to port...", end="")
ser = serial.Serial(port=args.port, baudrate=args.baud_rate)
time.sleep(5)
print(" done")

print("Initializing...", end="")
ser.write(b"IDXX")
time.sleep(10)
print(" done")

print("Moving to the force...", end="")
command = f"G00 K{args.force}"
ser.write(bytes(command, encoding='utf-8'))
time.sleep(50)
print(" done")

for _ in range(args.data_points):
    time.sleep(args.sleep_time)
    ser.write(b"M155")

ser.readlines(timeout=1)
