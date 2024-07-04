"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
import re
import exrex
import paramiko

def validate_min_max(min_val: int, max_val: int)-> tuple[int, int]:
    """
    Validate the min and max values.

    Args:
        min_val (int): The minimum length.
        max_val (int): The maximum length.

    Raises:
        argparse.ArgumentTypeError: If validation fails.
    """
    if min_val < 1 or max_val > 10 or min_val > max_val:
        raise argparse.ArgumentTypeError("Min must be >= 1, max must be <= 10, and min must be <= max.")
    return min_val, max_val


def read_words_list(word_list: str)-> list[str]:
    """
    Reads all content of word_list file

    Args:
        world_list (str): Path to word_list file

    Raises:
        argparse.ArgumentTypeError: If file not found
    """
    try:
        with open(word_list, 'r', encoding='utf-8') as file:
            words = file.read().splitlines()
        return words or []
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"No such file or directory: {word_list}")


def sanitize_pattern(pattern: str)-> str:
    """
    Sanitize the input regex pattern to be a basic one, removing any quantifiers or complex components.

    Args:
        pattern (str): The input regex pattern.

    Returns:
        str: The sanitized basic regex pattern.
    """
    # Remove any quantifiers {min,max}
    pattern = re.sub(r'\{\d+,\d+\}', '', pattern)
    # Remove other complex regex components like *, +, ?
    pattern = re.sub(r'[+*?]', '', pattern)
    # Ensure pattern is a simple character set (e.g., [a-z])
    basic_pattern = ''.join(re.findall(r'\[.*?\]', pattern))
    return basic_pattern


def generate_words_list(args: argparse.Namespace)-> list[str]:
    """
    Generates word_list from args.characterset
        within args.min and args.max range

    Args:
        args (str): Path to word_list file

    Raises:
        argparse.ArgumentTypeError: If file not found
    """
    min, max = validate_min_max(args.min, args.max)
    sanitized_pattern = sanitize_pattern(args.characterset)
    full_pattern = f"{sanitized_pattern}{{{min},{max}}}"
    generator = exrex.generate(full_pattern)
    words = ('\n'.join(generator)).splitlines()
    return words or []


def get_words(args: argparse.Namespace)-> list[str]:
    """
    Retrieve list of words based on given Command-line arguments.
        - If args.wordlist is given, return words from file
        - Else return generated words base on given args.characterset and range

    Args:
        args (argparse.Namespace): Passed args on script run
    """
    if args.wordlist:
        print(f"Using File {args.wordlist} to read words...")
        words = read_words_list(args.wordlist)
    else:
        print(f"Using Character set {args.characterset} to generate words...")
        words = generate_words_list(args)
    return words or []


def establish_connection(args: argparse.Namespace, password: str)-> paramiko.SSHClient | None:
    """
    Establishes an ssh connection to <args.username>@<args.server>

    Args:
        args (argparse.Namespace): Command-line arguments containing the username and server to connect to
        password (str): Credential for establishing ssh connection

    Returns:
        paramiko.SSHClient | None : SSH client if connection was established for further use, else closes the SSHClient
    """
    try:
        # Establish the connection
        ssh = paramiko.SSHClient()
        ssh.connect(args.server, username=args.username, password=password)
        return ssh
    except paramiko.AuthenticationException:
        print(f"Authentication failed, please verify your credentials!")
        ssh.close()
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
        ssh.close()
    except Exception as e:
        print(f"Operation error: {e}")
        ssh.close()