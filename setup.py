import serial
import serial.tools.list_ports as ports
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-lp", "--list-ports", help="List the available ports", action="store_true")
args = parser.parse_args()


def list_ports():
    print("Available ports:\n")
    com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
    for port in com_ports:
        print(f"Device {port.device} with name {port.name}")
    return com_ports

def connect_port(port):
    try:
        ser = serial.Serial(port)
    except serial.SerialException as error:
        print(error)
    else:
        return ser

if __name__ == "__main__":
    if args.list_ports:
        list_ports()
