"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
import os
from logger import init_logger, log_msg


def is_pdf_file(file_name: str) -> str:
    """
    Validates given file:
        1. Check if the file is a pdf type.
        1. Check if the file exists.

    Args:
        file_name (str) : File path to check.

    Returns:
        (str) : returns the given filename back.

    Raises:
        argparse.ArgumentTypeError :
            - If file is not a PDF file.
            - If file does not exist.
    """
    # Check if the file has a .pdf extension
    if not file_name.endswith(".pdf"):
        raise argparse.ArgumentTypeError(f"File '{file_name}' is not a PDF file.")

    # Check if the file exists and is readable
    if not os.path.isfile(file_name):
        raise argparse.ArgumentTypeError(f"File '{file_name}' does not exist.")

    return file_name


def resolve_name(args: argparse.Namespace):
    """
    Resolve name argument.
    If none is given the name of the file argument will be given.

    Args:
        args (argparse.Namespace) : Command Line Arguments
    """

    if not args.name:
        # Extract just the file name (without path and extension) from args.file
        args.name = os.path.splitext(os.path.basename(args.file))[0]


def validate_args(args: argparse.Namespace):
    """
    Validates Command-Line arguments.
    """
    resolve_name(args)


def init() -> argparse.Namespace:
    """
    Initializes Command-line arguments.

    Accepted arguments:
        -f --filename: (str) required,
        -d --destination: (str) required,
        -n --name: (str)
        --debug: (bool)

    Usage examples:
        Using PDF file name as CSV file name: $python metascan.py -f example.pdf -d outputs
        Using name argument value as CSV file name: $python metascan.py -f example.pdf -d outputs -n my_csv
    """
    log_msg("Initializing metascan...")
    parser = argparse.ArgumentParser(
        description="Metascan reads Meta-Data from a given PDF file and outputs them in CSV file."
    )
    parser.add_argument(
        "-f", "--file", required=True, type=is_pdf_file, help="PDF file input location"
    )
    parser.add_argument(
        "-d",
        "--destination",
        required=True,
        type=str,
        help="CSV file output destination",
    )
    parser.add_argument("-n", "--name", type=str, help="CSV file output name")
    parser.add_argument("--debug", action="store_true", help="Prints debug logs")

    args = parser.parse_args()
    init_logger(args)
    validate_args(args)
    return args
