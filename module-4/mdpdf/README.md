# My `mdpdf` Meta-Data Analytic Tool

This project automatically reads metadata from PDF files and writes them to a CSV file.

This lightweight implementation covers the following features/options:

- Extracts metadata from a given PDF file and writes the data to a CSV file.

## Table of content

- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Command-line arguments](#command-line-arguments)
- [Structure](#structure)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage Examples](#usage-examples)

## Technologies

- Windows 11
- Python 3.10.11
- `venv` (python virtual environment)

## Dependencies

- `pypdf==5.0.1`: Used to read and extract metadata from PDF files.

## Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `--file` | `-f` | PDF file input path | | str | x |
| `--destination` | `-d` | CSV file output directory | | str | x |
| `-n` | `--name` | CSV file output name | PDF file's original name | str | |
| `--debug` | | Flag to enable debug-level logging | | bool | |

## Structure

- [init.py](./init.py): Validates and initializes the command-line arguments.
- [logger.py](./logger.py): Contains logging functions used to log messages.
- [mdpdf.py](./mdpdf.py): Main file to run and pass command-line arguments.
- [utils.py](./utils.py): Helper functions to handle the passed command-line arguments.
- [requirements.txt](./requirements.txt): Contains dependencies.

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
# Start the mdpdf script
python mdpdf.py `
    -f <path_to/your_file.pdf> `    # e.g., example.pdf
    -d <path_to_output_directory/> ` # Output directory for the CSV file
    -n <name_of_csv_file> `         # Optional: If omitted, CSV file will be named after the PDF file
    --debug                         # Optional: Enables debug logs
```

This will generate a CSV file, `example.csv`, containing metadata from `example.pdf`.
