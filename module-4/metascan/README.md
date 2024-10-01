# My `metascan` Meta-Data Analytic Tool

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
- [Proof of Concept](#proof-of-concept)

## Technologies

- Windows 11
- Python 3.10.11
- `venv` (python virtual environment)

## Dependencies

- `pypdf==5.0.1`: Used to read and extract metadata from PDF files.
- `selenium==4.25.0`: TBD
- `requests==2.32.3` : TBD

## Command-line arguments

### Required Mutual Exclusive Group Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--file` | `-f` | PDF file input path | | str | x |
| `--url` | `-u` | URL to scan and download PDFs | | str | x |

### Single Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `--file` | `-f` | PDF file input path | | str | x |
| `--destination` | `-d` | CSV file output directory | | str | x |
| `-n` | `--name` | CSV file output name | | str | x |
| `--debug` | | Flag to enable debug-level logging | | bool | |

## Structure

- [init.py](./init.py): Initializes the command-line arguments.
- [logger.py](./logger.py): Contains logging functions used to log messages.
- [metascan.py](./metascan.py): Main file to run and pass command-line arguments.
- [utils.py](./utils.py): Helper functions to handle the passed command-line arguments.
- [requirements.txt](./requirements.txt): Contains dependencies.
- [demo_webapp/](./demo_webapp/): Used in the proof of concept.

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

#### Using PDF file input Argument

```powershell
# Start the metascan script
python metascan.py `
    -f <path_to/your_file.pdf> `     # e.g., example.pdf
    -d <path_to_output_directory/> ` # Output directory for the CSV file
    -n <name_of_csv_file> `          # CSV file output name e.g., example.csv
    --debug                          # Optional: Enables debug logs
```

This will generate a CSV file, `example.csv`, containing metadata from `example.pdf`.

#### Using URL input Argument

```powershell
# Start the metascan script
python metascan.py `
    -u <your-domain> `               # URL to scan and download PDFs
    -d <path_to_output_directory/> ` # Output directory for the CSV file
    -n <name_of_csv_file> `          # CSV file output name e.g., example.csv
    --debug                          # Optional: Enables debug logs
```

This will generate a CSV file, `example.csv`, containing metadata from all downloaded PDF files from given URL.

### Proof of Concept

1. Add two pdf files in `demo_webapp` folder and name them `example.pdf` and `example2.pdf`.

1. Build and run the demo app Docker images.

    ```powershell
    # In a terminal, navigate to the root of the metascan project.

    # Navigate to the demo_webapp folder.
    cd demo_webapp

    # Build the demo web app Docker image.
    docker build -t demo_webapp .

    # Run the demo web app image.
    docker run -it --rm `
        -p 8080:80 `
        --name demo_webapp `
        demo_webapp
    ```

1. Scan the demo apps using the metascan tool.

```powershell
# In a terminal, navigate to the root of the metascan project.

# Run metascan
python metascan.py `
    -u http:localhost:8080 `  # Demo Web page URL
    -d output `               # Destination of download PDF files from Demo Web page and CSV file output.
    -n localhost_8080         # CSV file output name.
```
