# My `hydra clone` tool

This folder contains the source code for my own implementation of the `hydra` tool.
**Hydra** clone can be used to connect to servers via SSH using a list of passwords, either generated from a character set or provided via a wordlist file.

This lightweight implementation covers the following features/options:

- Connect to a server via SSH using a wordlist as passwords.
- Generate a list of words from a basic character set or use a file containing passwords.

## Table of content

- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Command-line arguments](#command-line-arguments)
- [Structure](#structure)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Prove of Concept](#prove-of-concept)

## Technologies

- Windows 11
- Python 3.10.11
- `venv` (python virtual environment)
- Docker (optionally for proof of concept)

## Dependencies

- `exrex==0.11.0`: Used to generate all possible combinations of words from a given character set.
- `paramiko==3.4.0`: Used for connecting to a server as a user via SSH.

## Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `--username` | `-u` | Username to connect | | str | x |
| `--server` | `-s` | Server IP address or DNS name to connect | | str | x |
| `--port` | `-p` | SSH Port | 22 | int | |
| `--wordlist` | `-w` | Wordlist file used as dictionary | | str | |
| `--characterset` | `-c` | Character set used to generate passwords | [a-z] | str | |
| `--min` | | Minimum generated word length | 3 | int | |
| `--max` | | Maximum generated word length | 3 | int | |

## Structure

- [hydra.py](./hydra.py): Main file to run the tool and pass command-line arguments.
- [ini.py](./init.py): Initializes and validates command-line arguments.
- [utils.py](./utils.py): Functions for validating arguments, generating words from the character set, and reading words from a wordlist.
- [requirements.txt](./requirements.txt): Contains dependencies.
- [Dockerfile](./Dockerfile): Creates a simple target machine to test SSH connections, with build arguments for SSH port and root user password.
- [dictionary.txt](./dictionary.txt): Used in the [Prove of concept](#prove-of-concept) example.

## Getting Started

### Installation

```powershell
# Create and activate Python virtual environment
python -m venv venv
./venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage examples

```powershell
# Start hydra using default options (Brute-force with character set)
python hydra.py `
    -u <username> `      # e.g., root
    -s <remoteserver> `  # e.g., 123.45.67.89
```

This generates a list of all possible combinations of lowercase letters (a-z) with a minimum and maximum length of 3, and attempts to connect to the server using each combination as a password.

```powershell
# Start hydra using a custom character set with a defined word length
python hydra.py `
    -u <username> `      # e.g., root
    -s <remoteserver> `  # e.g., 123.45.67.89
    -c [a-z0-9] `        # Character set: lowercase letters and digits (a-z, 0-9)
    --min 5 `            # Minimum word length
    --max 5              # Maximum word length
```

This generates a list of all possible combinations of lowercase letters and digits (a-z, 0-9) with a word length of 5 and tries each combination as a password.

```powershell
# Start hydra using a wordlist as a dictionary
python hydra.py `
    -u <username> `      # e.g., root
    -s <remoteserver> `  # e.g., 123.45.67.89
    -w dictionary.txt    # Wordlist file
```

This reads passwords from `dictionary.txt` and attempts to connect to the server using each password.

Once the password list is prepared, Hydra loops through the words and attempts to establish a connection via SSH. If successful, the password is printed, and the command whoami is executed to confirm the connection.

### Prove of Concept

The following example demonstrates how to use the Hydra clone tool to connect to a Docker container via SSH.

```powershell
# Build the target machine (Docker container)
docker build `
    --build-arg PORT=2222 `
    --build-arg PASSWORD=changeme `
    -t python-ssh .

# Add the password 'changeme' to dictionary.txt

# Run the target machine (Docker container)
docker run -d `
    --name python-ssh-container `
    -p 2222:2222 `
    python-ssh

# Ensure the Python environment is activated on the host machine, then run Hydra:
python hydra.py `
    -u root `
    -s localhost `
    -p 2222 `
    -w dictionary.txt

# Expected output:
Initializing Hydra Clone...
Getting words...
Using file dictionary.txt to read words...
Got 1 Word(s)...
Starting connections to localhost as root...
Please wait...
Connection 1 established! Password -> changeme
Executing command 'whoami'...
Command response: root

Closing SSH Client...
Hydra Exited!
```

If you do not see the output above, ensure `dictionary.txt` contains the password `changeme`.

#### Try binding to different ports

```powershell
# Stop and remove the container
docker stop python-ssh-container
docker rm python-ssh-container

# Start the container with a different port binding:
docker run -d `
    --name python-ssh-container `
    -p 8888:2222 `
    python-ssh

# Run Hydra again:
python hydra.py `
    -u root `
    -s localhost `
    -p 8888 `
    -w dictionary.txt
```
