# My `nmap clone` tool

This is my own implementation of the `nmap` tool.
Can be used to scan an IP- or DNS-Address for opened ports.

This is a lightweight implementation that covers the following features/options:

- Finds open ports using various TCP connections.
- For the first 100 ports scans finds the running application type.

## Table of content

- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Command-line arguments](#command-line-arguments)
- [Structure](#structure)
- [Getting started](#getting-started)
- [Installation](#installation)
- [Usage examples](#usage-examples)
- [Prove of concept](#prove-of-concept)

## Technologies

- Windows 11
- Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
- venv (python virtual environment)
- Docker (optionally for prove of concept)

## Dependencies

- scapy==2.5.0: used to perform various tcp scans technics

## Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `--port` | `-p` | Port Range | | str | x |
| `--address` | `-a` | Server as IP-Address or DNS name to connect | | str | x |
| `--debug` | `-d` | Flag to print debug level prints | | bool | |

## Structure

- [enums.py](./enums.py): TCP Flags Enums.
- [init.py](./init.py): Validates and initializes the command-line arguments.
- [literals.py](./literals.py): Defines Literals for each TCP Scan Technic.
- [logger.py](./logger.py): Contains logging function used across nmap to log messages.
- [nmap.py](./nmap.py): Main file to run and pass command-line arguments.
- [scans.py](./scans.py): Definitions of various TCP Scans Technics.
- [scapy_utils.py](./scapy_utils.py): Wrapper functions that use scapy.
- [utils.py](./utils.py): Core functions of nmap.
- [requirements.txt](./requirements.txt): contains dependencies.
- [scan_application.py](./scan_application.py): Scans for application listing on a given address and port.
- [demo_webapp/](./demo_webapp/): Used in prove of concept.
- [demo_sshapp/](./demo_sshapp/): Used in prove of concept.

## Getting started

### Installation

```powershell
# Create and activate python virtual environment
python -m venv venv
venv/Scripts/activate

# Activate python environment
./venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage examples

```powershell
# Start hydra using defaults
python nmap.py `
    -p <port-range> `   # port range: 80, 0-2222, -
    -a localhost `      # address: 123.45.67.89, your-domain.com
    -d                  # if given more logs are printed
```

This will scan the address's given ports if opened and for first 100 will scan the application type.

### Prove of concept

1. Build and run the demo apps Docker images.

    ```powershell
    # Open a new terminal in the root of nmap locations.

    # Navigate to demo_webapp folder.
    cd demo_webapp

    # Build demo webapp image.
    docker build demo_webapp .

    # Run demo webapp image.
    docker run -it --rm `
        -p 8080:80 `
        --name demo_webapp `
        demo_webapp

    # Open a new terminal in the root of nmap locations.

    # Navigate to demo_sshapp folder.
    cd demo_sshapp

    # Build demo webapp image.
    docker build demo_sshapp .

    # Run demo webapp image.
    docker run -it --rm `
        -p 2222:22 `
        --name demo_sshapp `
        demo_sshapp
    ```

1. Scan demo apps using nmap

    ```powershell
    # Open a new terminal in the root of nmap locations.

    # Scan the demo webapp.
    python nmap.py `
        -p 8080 `
        -a 127.0.0.1

    # Output Example
    [2024.09.29 09:07:20]   [INFO]  [Initializing Nmap Clone...]
    [2024.09.29 09:07:20]   [INFO]  [Finding opened ports ...]
    [2024.09.29 09:07:22]   [INFO]  [Host 127.0.0.1 Port 8080: Open]
    [2024.09.29 09:07:22]   [INFO]  [Scanning APPLICATION...]
    [2024.09.29 09:07:27]   [WARNING]       [Timeout on port 8080, retrying... (1 retries left)]
    [2024.09.29 09:07:27]   [INFO]  [Scanning APPLICATION...]
    [2024.09.29 09:07:29]   [INFO]  [APPLICATION: Nginx Web Server]
    [2024.09.29 09:07:29]   [INFO]  [Scanning OS...]
    [2024.09.29 09:07:31]   [INFO]  [OS: Windows (Unknown OS)]

    # Scan the demo sshapp
    python nmap.py `
        -p 2222 `
        -a 127.0.0.1

    # Output Example
    [2024.09.29 09:10:02]   [INFO]  [Initializing Nmap Clone...]
    [2024.09.29 09:10:02]   [INFO]  [Finding opened ports ...]
    [2024.09.29 09:10:04]   [INFO]  [Host 127.0.0.1 Port 2222: Open]
    [2024.09.29 09:10:04]   [INFO]  [Scanning APPLICATION...]
    [2024.09.29 09:10:06]   [INFO]  [APPLICATION: OpenSSH Server]
    [2024.09.29 09:10:06]   [INFO]  [Scanning OS...]
    [2024.09.29 09:10:06]   [INFO]  [OS: Windows (Unknown OS)]
    ```
