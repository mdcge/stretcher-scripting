# Stretcher scripting

This repository provides basic scripts which can be used to automate sending commands to the fibre stretcher. Included below are instructions to setting this up.

## Nix and prerequisites

You will notice that there is a `.nix` file in the repository. Unless you are using Nix (which would be great, as this will work out-of-the-box for you), feel free to ignore these files (`flake.nix`, `flake.lock` and `.envrc`).

If you are not using Nix, you will need the following prerequisites:

- `pyserial`

## Setting up the connection

**This must be performed in the native operating system of the serial port.** For example, it will not work in a WSL on Windows.

The first step is to establish the connection with the stretcher. To do this, the `setup.py` script can be used in the following ways:

- `python setup.py --list-ports`: lists the ports available to the machine.
- `python setup.py --port-index <idx>`: connects to the serial port of index `idx`. The indices of each port are shown with the `--list-ports` flag.
- `python setup.py --port-name <name>`: connects to the serial port with called `name`. The names of each port are shown with the `--list-ports` flag.

## Running commands

The `command.py` script can be used to submit a command to the stretcher. Some things to keep in mind when controlling the stretcher from a script:

- Once the script reaches its end, the stretcher will immediately stop any action it was performing. It is therefore advisable to use the `sleep` command liberally. This is not a problem if interfacing with the stretcher from the python prompt directly.
- The connection to the serial port seems to need about 5 seconds to establish properly. A `sleep(5)` is recommended just after the opening the serial connection.
- <span style="color:red">[Still testing]</span> If a new command is written to the serial port before the previous one has finished, it will store it and perform it when the previous one has finished. However, if another command is written before the original one has completed, it will overwrite any other commands waiting in the queue.

The `command.py` script will sleep for an hour after the desired command is performed. In most cases, this will be unwanted, so just interrupt the script (with `C-c` for example).
