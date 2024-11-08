import serial
import serial.tools.list_ports as prts
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-lp", "--list-ports", help="List the available ports", action="store_true")
parser.add_argument("-pi", "--port-index", help="Index of the port to connect to", type=int)
parser.add_argument("-pn", "--port-name", help="Name of the port to connect to", type=str)
args = parser.parse_args()


def list_ports():
    print("Available ports:\n")
    ports = list(prts.comports())
    for i, port in enumerate(ports):
        print(f"Device {port.device} with name {port.name}   -> ({i})")
    return ports

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
    if args.port_index is not None:
        ports = list_ports()
        print()
        ser = connect_port(ports[args.port_index].name)
        ser.close()
    if args.port_name is not None:
        ports = list_ports()
        print()
        ser = connect_port(args.port_name)
        ser.close()
