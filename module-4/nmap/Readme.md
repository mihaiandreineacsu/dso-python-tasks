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

- [nmap.py](./nmap.py): Main file to run and pass command-line arguments
- [init.py](./init.py): validates and initializes the command-line arguments
- [utils.py](./utils.py):
- [requirements.txt](./requirements.txt): contains dependencies

