"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import csv
from pypdf import PdfReader
from logger import log_msg


def extract_metadata(file: str) -> dict[str, str]:
    """
    Extract metadata from a single PDF file.

    Args:
        file (str) : Path to file from which to extract meta-data.

    Returns:
        dict[str, str] : A custom defined dict containing the meta-data.
    """
    log_msg("Extracting Meta-Data...")
    with open(file, "rb") as input_file:
        pdf = PdfReader(input_file)
        metadata = pdf.metadata
        header = pdf.pdf_header

        # Handle missing or None metadata fields
        doc_info = {
            "Title": metadata.title if metadata.title else "Unknown",
            "Author": metadata.author if metadata.author else "Unknown",
            "Creator": metadata.creator if metadata.creator else "Unknown",
            "Created": metadata.creation_date if metadata.creation_date else "Unknown",
            "Modified": (
                metadata.modification_date if metadata.modification_date else "Unknown"
            ),
            "Subject": metadata.subject if metadata.subject else "Unknown",
            "Keywords": (
                metadata.keywords if hasattr(metadata, "keywords") else "Unknown"
            ),  # Safely handle 'Keywords'
            "Description": (
                metadata.description if hasattr(metadata, "description") else "Unknown"
            ),  # Safely handle 'Description'
            "Producer": metadata.producer if metadata.producer else "Unknown",
            "PDF Version": header if header else "Unknown",
        }

        log_msg(f"Metadata: {metadata}, Header: {header}", "DEBUG")
        return doc_info


def output_doc_info(doc_info: dict[str, str], destination: str, name: str):
    """
    Write document information to CSV file.

    Args:
        doc_info (dict[str, str]) : A dictionary containing Document Information.
        destination (str) : Path to the directory where the CSV file will be saved.
        name (str) : The name of the output CSV file.
    """
    full_path_destination = f"{destination}/{name}.csv"
    log_msg("Outputting Document Information...")
    with open(
        full_path_destination, "w", newline="", encoding="utf-8"
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=doc_info.keys(), delimiter=";")
        writer.writeheader()
        # Write the single doc_info dictionary to the CSV file
        writer.writerow(doc_info)
        log_msg(f"Document Information saved to {full_path_destination}")
