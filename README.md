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

### Available commands

These are the available commands recognised by the stretcher (connection method-agnostic):

| Command | Effect |
| :----: | :----: |
| IDXX | Initialize stretcher |
| G28 | "Home" the stretcher |
| M155 | Measure |
| G00 Kx | Move the stretcher to $$x$$ newtons of force |
| G00 Xd | Move the stretcher to $$d$$ increments |

100 increments = 0.25mm 

### Running commands from scripts

Some things to keep in mind when controlling the stretcher from a script:

- Once the script reaches its end, the stretcher will immediately stop any action it was performing. It is therefore advisable to use the `sleep` command liberally. This is not a problem if interfacing with the stretcher from the python prompt directly.
- The connection to the serial port seems to need about 5 seconds to establish properly. A `sleep(5)` is recommended just after the opening the serial connection.
- ${\color{red}\text{[STILL TESTING]}}$ If a new command is written to the serial port before the previous one has finished, it will store it and perform it when the previous one has finished. However, if yet another command is written before the original one has completed, it will overwrite any other commands waiting in the queue.
- The `IDXX` command must always be called as the first command of a script, otherwise no other commands will be registered by the stretcher.

## Scripts

### `command.py`

The `command.py` script can be used to submit a single command to the stretcher. It takes 3 command-line arguments:

- `-p`/`--port`: name of the port to connect to (obtained with `setup.py`)
- `-c`/`--command`: command to pass to the stretcher
- `-br`/`--baud-rate` [optional]: baud rate of the connection (default = 115200) 

The `command.py` script will sleep for an hour after the desired command is performed. In most cases, this will be unwanted, so just interrupt the script (with `C-c` for example).
