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


def init() -> argparse.Namespace:
    """
    Initializes Command-line arguments.

    Accepted arguments:
        -f --filename: (str)
        --debug: (bool)

    Usage examples: $python metaclean.py -f example.pdf
    """
    log_msg("Initializing metaclean...")
    parser = argparse.ArgumentParser(description="Meta Clean removes Meta-Data from a given PDF file.")
    parser.add_argument("-f", "--file", type=is_pdf_file, help="PDF file input location.")
    parser.add_argument("--debug", action="store_true", help="Prints debug logs.")

    args = parser.parse_args()
    init_logger(args)
    return args
