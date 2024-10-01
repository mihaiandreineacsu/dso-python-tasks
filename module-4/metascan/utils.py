"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import csv
import os
import time
from pypdf import PdfReader
from logger import log_msg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests


def download_pdfs(url: str, destination: str) -> list[str]:
    """
    Downloads all PDFs from the given Website URL using Selenium.

    Args:
        url (str): URL to download PDFs from.
        destination (str): Locations to download PDFs to.

    Returns:
        list[str]: Downloaded files paths.
    """

    log_msg(f"Searching for PDFs on {url}...")
    if not os.path.exists(destination):
        os.makedirs(destination)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("-private")  # Enable private browsing
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    time.sleep(2)

    pdf_links = driver.find_elements(By.CSS_SELECTOR, 'a[href$=".pdf"]')
    log_msg(f"Found {len(pdf_links)} PDF Links...")

    files = []  # Keep track of downloaded files location
    for link in pdf_links:
        pdf_url = link.get_attribute("href")
        pdf_response = requests.get(pdf_url)

        pdf_name = os.path.join(destination, os.path.basename(pdf_url))

        with open(pdf_name, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
            files.append(pdf_name)

    driver.delete_all_cookies()  # Clear all cookies in Chrome/Firefox/Edge
    driver.quit()
    return files


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
    file_exists = os.path.exists(full_path_destination)
    log_msg("Outputting Document Information...")

    with open(full_path_destination, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=doc_info.keys(), delimiter=";")

        # Write the header only if the file does not already exist
        if not file_exists:
            writer.writeheader()

        # Write the single doc_info dictionary to the CSV file
        writer.writerow(doc_info)
        log_msg(f"Document Information saved to {full_path_destination}")
