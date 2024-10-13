"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
import os
import subprocess
from typing import Union
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
        result = run_subprocess(["exiftool", f"{args.file}"], check=True)
        log_msg(f"\n{result.stdout}", "DEBUG")
        # Potential security risk: args.file is an user input and this runs in shell.
        result = run_subprocess(f"exiftool {args.file} | wc -l", shell=True, check=True)
        log_msg(f"{result.stdout}", "DEBUG")


def run_subprocess(
    args: Union[str, bytes, os.PathLike],
    on_error_message: str = None,
    shell: bool = False,
    cwd: str = None,
    encoding: str = None,
    timeout: float = None,
    check: bool = False,  # Adds a check parameter to raise an exception if returncode is non-zero
    input: str = None,  # Adds input parameter to pass data to stdin
) -> subprocess.CompletedProcess[str]:
    """
    Wrapper function that calls subprocess.run with given arguments.

    Args:
        args (tuple) : Arguments to pass to subprocess.run.
        on_error_message (str) : Custom error message to log when subprocess fails.
        shell (bool) : Sets the shell flag of subprocess.run.
        cwd (str): The directory from which to run the command. Defaults to None.
        encoding (str): Specifies encoding for the output.
        timeout (float): Specifies timeout for subprocess.run.
        check (bool): If True, raise a CalledProcessError on non-zero exit code.
        input (str): Data to send to the subprocess' stdin.

    Raises:
        RuntimeError: When subprocess.run returns a non-zero exit code and check is False.
        subprocess.CalledProcessError: If check is True and a non-zero exit code occurs.

    Returns:
        subprocess.CompletedProcess[str] : Result of subprocess.run.
    """

    if shell:
        log_msg(f"Potential security risk: args {args} is running in shell!", "WARNING")

    try:
        # Pass the input argument if specified
        result = subprocess.run(
            args,
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Treat stdout, stderr, and input as text (str)
            shell=shell,  # Run in shell if needed
            cwd=cwd,  # Working directory
            encoding=encoding,  # Encoding for input and output
            timeout=timeout,  # Timeout for the process
            input=input,  # Input data for stdin
            check=check,  # Raise error if command fails (non-zero exit code)
        )
        return result

    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"Subprocess timed out: {e}")

    except subprocess.CalledProcessError as e:
        if not on_error_message:
            on_error_message = str(args)
        raise RuntimeError(f"{on_error_message}: {e.stderr.strip()}")

    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


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
    run_subprocess(
        ["exiftool", "-all=", f"{file}", "-o", "tmp.pdf"], on_error_message="Remove Metadata failed", check=True
    )
    # Linearize the PDF (ensure this doesn't add metadata)
    run_subprocess(
        ["qpdf", "--linearize", "tmp.pdf", "document.clean.pdf"], on_error_message="Linearization failed", check=True
    )

    log_msg("Removing tmp and original files...")
    run_subprocess(["rm", "tmp.pdf"], on_error_message="Removing tmp file failed", check=True)
    run_subprocess(["rm", f"{file}"], on_error_message="Removing original file failed", check=True)

    return "document.clean.pdf"
