# My `nmap clone` tool

This is my own implementation of the `nmap` tool, used to scan an IP or DNS address for open ports and identify the running applications on those ports.

This lightweight implementation covers the following features/options:

- Find open ports using various TCP scan techniques.
- For the first 100 ports, identify the type of running application.

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
- Docker (optionally for prove of concept)

## Dependencies

- `scapy==2.5.0`: Used to perform various TCP scan techniques.

## Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `--port` | `-p` | Port range to scan | | str | x |
| `--address` | `-a` | Server IP address or DNS name to scan | | str | x |
| `--debug` | `-d` | Enable debug-level logging for more output detail | | bool | |

## Structure

- [enums.py](./enums.py): Contains TCP flag enums.
- [init.py](./init.py): Validates and initializes the command-line arguments.
- [literals.py](./literals.py): Defines literals for each TCP scan technique.
- [logger.py](./logger.py): Contains the logging functionality for the tool.
- [nmap.py](./nmap.py): Main file to run the tool and pass command-line arguments.
- [scans.py](./scans.py): Contains definitions of various TCP scan techniques.
- [scapy_utils.py](./scapy_utils.py): Wrapper functions that utilize Scapy.
- [utils.py](./utils.py): Core functions of the nmap clone tool.
- [requirements.txt](./requirements.txt): Contains dependencies.
- [scan_application.py](./scan_application.py): Scans for the application running on a given address and port.
- [demo_webapp/](./demo_webapp/): Used in the proof of concept.
- [demo_sshapp/](./demo_sshapp/): Used in the proof of concept.

## Getting Started

### Installation

```powershell
# Create and activate the Python virtual environment
python -m venv venv
./venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage Examples

```powershell
# Scan a specific port range on an address
python nmap.py `
    -p <port-range> `   # Port range: 80, 0-2222, or just -
    -a localhost `      # Address: 127.0.0.1, 123.45.67.89, your-domain.com
    -d                  # Enable debug output (optional)
```

This scans the specified ports on the address and, for the first 100 ports, attempts to identify the running application.

### Prove of Concept

1. Build and run the demo app Docker images.

    ```powershell
    # In a terminal, navigate to the root of the nmap clone project.

    # Navigate to the demo_webapp folder.
    cd demo_webapp

    # Build the demo web app Docker image.
    docker build -t demo_webapp .

    # Run the demo web app image.
    docker run -it --rm `
        -p 8080:80 `
        --name demo_webapp `
        demo_webapp

    # Open another terminal and navigate to the demo_sshapp folder.
    cd demo_sshapp

    # Build the demo SSH app Docker image.
    docker build -t demo_sshapp .

    # Run the demo SSH app image.
    docker run -it --rm `
        -p 2222:22 `
        --name demo_sshapp `
        demo_sshapp

    ```

1. Scan the demo apps using the nmap clone tool.

    ```powershell
    # In a terminal, navigate to the root of the nmap clone project.

    # Scan the demo web app on port 8080.
    python nmap.py `
        -p 8080 `
        -a 127.0.0.1

    # Example Output:
    [2024.09.29 09:07:20]   [INFO]  [Initializing Nmap Clone...]
    [2024.09.29 09:07:20]   [INFO]  [Finding open ports ...]
    [2024.09.29 09:07:22]   [INFO]  [Host 127.0.0.1 Port 8080: Open]
    [2024.09.29 09:07:22]   [INFO]  [Scanning application...]
    [2024.09.29 09:07:27]   [WARNING]  [Timeout on port 8080, retrying... (1 retry left)]
    [2024.09.29 09:07:27]   [INFO]  [Scanning application...]
    [2024.09.29 09:07:29]   [INFO]  [Application: Nginx Web Server]
    [2024.09.29 09:07:29]   [INFO]  [Scanning OS...]
    [2024.09.29 09:07:31]   [INFO]  [OS: Windows (Unknown OS)]

    # Scan the demo SSH app on port 2222.
    python nmap.py `
        -p 2222 `
        -a 127.0.0.1

    # Example Output:
    [2024.09.29 09:10:02]   [INFO]  [Initializing Nmap Clone...]
    [2024.09.29 09:10:02]   [INFO]  [Finding open ports ...]
    [2024.09.29 09:10:04]   [INFO]  [Host 127.0.0.1 Port 2222: Open]
    [2024.09.29 09:10:04]   [INFO]  [Scanning application...]
    [2024.09.29 09:10:06]   [INFO]  [Application: OpenSSH Server]
    [2024.09.29 09:10:06]   [INFO]  [Scanning OS...]
    [2024.09.29 09:10:06]   [INFO]  [OS: Windows (Unknown OS)]

    ```
