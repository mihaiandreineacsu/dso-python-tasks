# My `metaclean` Meta-Data Tool

This project automatically cleans critical metadata from PDF files.

This lightweight implementation covers the following features/options:

- Removes metadata from a given PDF file.

## Table of content

- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Command-line-arguments](#command-line-arguments)
- [Structure](#structure)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage Examples](#usage-examples)

## Technologies

- Docker version 27.2.0
- Python

### Why Docker?

Docker provides an isolated environment to ensure all dependencies, like `exiftool` and `qpdf`, are installed and configured properly, so you don't have to worry about system-specific issues.

## Dependencies

- `exiftool`: Used to read and remove metadata from PDF files.
- `qpdf`: Used to linearize PDF files.

## Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `--file` | `-f` | PDF file input path | | str | x |
| `--debug` | | Flag to enable debug-level logging | | bool | |

## Structure

- [init.py](./app/init.py): Initializes the command-line arguments.
- [logger.py](./app/logger.py): Contains logging functions used to log messages.
- [metaclean.py](./app/metaclean.py): Main file to run and pass command-line arguments.
- [utils.py](./app/utils.py): Helper functions to handle the passed command-line arguments.
- [Dockerfile](./Dockerfile): This Dockerfile creates an image based on the latest Ubuntu, setting up a lightweight environment for the /metaclean application. The default command starts a bash shell.

## Getting Started

### Installation

```powershell
# Build Dockerfile
docker build -t metaclean . # You can name the Docker image whatever you like.
```

### Usage Examples

#### Using PDF file input Argument

```powershell
# Start the metaclean Docker container

docker run -it `               # Start an interactive bash terminal inside the container.
    -v ${PWD}/app:/metaclean ` # Map host app directory to Docker container.
    metaclean                  # Name of the Docker image.
```

```bash
# Once inside the container, you can run the following:

python metaclean.py \
    -f <path_to/your_file.pdf> \    # Specify the file path inside the container.
    --debug                         # Optional: Enables debug logs.
```

The cleaned file `document.clean.pdf` will be saved directly in the `/metaclean` folder, which is already accessible from your host system.
