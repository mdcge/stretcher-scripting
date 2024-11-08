import serial
import sys

params = sys.argv
command = params[1]

# ser = serial.Serial(
#     port="COM4",
#     baudrate=115200,
#     parity=serial.PARITY_ODD,
#     stopbits=serial.STOPBITS_TWO,
#     bytesize=serial.SEVENBITS
# )

print(command)
