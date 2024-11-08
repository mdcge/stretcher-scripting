# Stretcher scripting

This repository provides basic scripts which can be used to automate sending commands to the fibre stretcher. Included below are instructions to setting this up.

## Nix and prerequisites

You will notice that there is a `.nix` file in the repository. Unless you are using Nix (which would be great, as this will work out-of-the-box for you), feel free to ignore these files (`flake.nix`, `flake.lock` and `.envrc`).

If you are not using Nix, you will need the following prerequisites:

- `pyserial`

## Necessary parameters

The baudrate (115200 for example) and port (COM4 for example) need to be known to establish the serial port connection.
