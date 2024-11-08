# Stretcher scripting

This repository provides basic scripts which can be used to automate sending commands to the fibre stretcher. Included below are instructions to setting this up.

## Nix and prerequisites

You will notice that there is a `.nix` file in the repository. Unless you are using Nix (which would be great, as this will work out-of-the-box for you), feel free to ignore these files (`flake.nix`, `flake.lock` and `.envrc`).

If you are not using Nix, you will need the following prerequisites:

- `pyserial`

## Setting up the connection

The first step is to establish the connection with the stretcher. To do this, the `setup.py` script can be used in the following ways:

- `python setup.py --list-ports`: lists the ports available to the machine.
- `python setup.py --port-index <idx>`: connects to the serial port of index `idx`. The indices of each port are shown with the `--list-ports` flag.
- 

The baudrate (115200 for example) and port (COM4 for example) need to be known to establish the serial port connection.
