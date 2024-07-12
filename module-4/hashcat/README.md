# My `hash clone` tool

This folder contains the source code for my own implementation of the `hydra` tool.
Hash clone can be used to TBD.

This is a lightweight implementation that covers the following features/options:

- ...
- ...

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

## Dependencies

## Command-line arguments

### Single Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory | Choices |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--mode` | `-m` | Hashmodes MD5 (0), SHA-1 (1), SHA-256 (2) and SHA-512 (3) | 0 | int | | {0, 1, 2, 3} |
| `--attack` | `-a` | Attack modes Brute-Force Attack (0) and Dictionary Attack (1) | 0 | int | | {0, 1} |

### Mutual exclusive Group required Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory | Choices |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--hash` | `-h` | Hash from direct input | | str |  |  |
| `--hashfile` | `-H` | Hash from file | | str |  |  |

## Structure

- [hashcat.py](./hashcat.py): Main file to run and pass command-line arguments
- [ini.py](./init.py): initializes the command-line arguments
- [utils.py](./utils.py): TBD
- [logger.py](./logger.py): Logs formatted messages

## Getting started

### Installation

### Usage examples

### Prove of concept
