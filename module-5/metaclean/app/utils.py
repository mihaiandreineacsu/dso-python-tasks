"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
import os
import subprocess
from logger import log_msg


def log_metadata(args: argparse.Namespace):
    """
    If debug argument is set it will:
        1. Print the given PDF file's metadata.
        2. Print the total number of PDF file's metadata.

    Args:
        args (args: argparse.Namespace) : Command-line Arguments passed to script.
    """
    if args.debug:
        # Check the resulting metadata after cleaning
        result = run_subprocess(["exiftool", f"{args.file}"])
        log_msg(f"\n{result.stdout}", "DEBUG")
        # Potential security risk: args.file is an user input and this runs in shell.
        result = run_subprocess(f"exiftool {args.file} | wc -l", shell=True)
        log_msg(f"{result.stdout}", "DEBUG")


def run_subprocess(
    args: str | bytes | os.PathLike,
    on_error_message: str = None,
    shell: bool = False,
    cwd: str = None,
    encoding: str = None,
) -> subprocess.CompletedProcess[str]:
    """
    Wrapper function that calls subprocess.run with given arguments.

    Args:
        args (tuple) : Arguments to pass on subprocess.run.
        on_error_message (str) : Custom error message to log when subprocess fails.
        shell (bool) : Sets the shell Flag of subprocess.run.
        cwd (str): The directory from which to run the command. Defaults to None.
        encoding (str): Specifies encoding for the output

    Raises:
        RuntimeError: When subprocess.run returns a non-zero exit code.

    Returns:
        subprocess.CompletedProcess[str] : Result of subprocess.run.
    """

    if shell:
        log_msg(f"Potential security risk: args {args} is runs in shell!", "WARNING")

    result = subprocess.run(args, capture_output=True, text=True, shell=shell, cwd=cwd, encoding=encoding)
    if result.returncode != 0:
        # Log error with custom message and stderr
        if not on_error_message:
            on_error_message = str(args)
        raise RuntimeError(f"{on_error_message}: {result.stderr.strip()}")
    return result


def clean_metadata(file: str):
    """
    Removes Meta-Data from given file.

    Args:
        file (str) : File location to remove meta data from.

    Returns:
        str : Name of the clean PDF file.
    """

    log_msg("Cleaning Metadata...")
    # First, remove metadata with ExifTool
    run_subprocess(["exiftool", "-all=", f"{file}", "-o", "tmp.pdf"], "Remove Metadata failed")
    # Linearize the PDF (ensure this doesn't add metadata)
    run_subprocess(["qpdf", "--linearize", "tmp.pdf", "document.clean.pdf"], "Linearization failed")

    log_msg("Removing tmp and original files...")
    run_subprocess(["rm", "tmp.pdf"], "Removing tmp file failed")
    run_subprocess(["rm", f"{file}"], "Removing original file failed")

    return "document.clean.pdf"
