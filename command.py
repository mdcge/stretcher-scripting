import serial
import serial.tools.list_ports as ports
import sys

params = sys.argv
command = params[1]

ser = serial.Serial(port="COM4", baudrate=115200)
ser.write(command)
ser.close()
