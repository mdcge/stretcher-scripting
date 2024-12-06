import serial
import argparse
import time


# Parse arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Port name", type=str)
parser.add_argument("-br", "--baud-rate", help="Baud rate of the connection", type=int, default=115200)
parser.add_argument("-f", "--force", help="Force to set the stretcher to", type=float)
parser.add_argument("-dp", "--data-points", help="Number of times to measure the force", type=int)
parser.add_argument("-s", "--sleep-time", help="Time between measurements", type=int)
args = parser.parse_args()

# Connect to port ---
print("Connecting to port...", end="", flush=True)
ser = serial.Serial(port=args.port, baudrate=args.baud_rate, timeout=1)
time.sleep(5)
print(" done")

# Initialize (IDXX) ---
print("Initializing...", end="", flush=True)
ser.write(b"IDXX")
time.sleep(15)
print(" done")

# Move to desired force ---
print("Moving to the force...", end="", flush=True)
command = f"G00 K{args.force}"
ser.write(bytes(command, encoding='utf-8'))
time.sleep(40)
print(" done")

# Open output file ---
with open("measurements.csv", 'w') as f:
    f.write("")

# Take measurements ---
current_data_point = 0
for i in range(args.data_points*10):
    # Wait
    if i != 0:
        time.sleep(args.sleep_time - 1)

    # Take measurement
    print(f"Taking measurement {i+1} of {args.data_points}")
    ser.write(b"M155")
    time.sleep(0.5)

    output = ser.readlines()
    measurements = list(map(lambda x: x.strip(), list(map(lambda x: x.decode("utf-8"), list(filter(lambda x: x[:3] == b"CFN", output))))))
    measured_force = float(measurements.split('N')[1].split('W')[0])
    force_command = f"G00 X{int(100 * (args.force - measured_force))}"
    ser.write(bytes(force_command, encoding='utf-8'))
    time.sleep(0.5)

    # Write output
    if i % 10 == 0:
        with open("measurements.csv", 'a') as f:
            for m in measurements:
                f.write(m + "\n")

# Return stretcher to home position ---
ser.write(b"G28")
time.sleep(20)
ser.close()
