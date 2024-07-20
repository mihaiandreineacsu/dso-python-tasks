"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
from logger import log_msg
import re
import enums


def validate_args(args: argparse.Namespace):
    MAX_PORT = enums.RangeEnum.MAX_PORT.value

    log_msg(f"ARGS PORT: {args.ports}", level="DEBUG")

    # Regex to validate port range format
    port_range_regex = re.compile(r'^(?:(\d{1,5})-(\d{1,5})|(\d{1,5})|(-))$')
    match = port_range_regex.match(args.ports)
    if not match:
        raise argparse.ArgumentTypeError(f"Invalid port range format: {args.ports}")
    start, end, single_port, hyphen = match.groups()

    log_msg(f"start {start}, end {end}, single_port {single_port}, hyphen {hyphen}", level="DEBUG")

    if hyphen:
        args.ports_list = list(range(MAX_PORT + 1))
    elif single_port:
        single_port = int(single_port)
        if single_port > MAX_PORT:
            raise ValueError(f"Invalid port: {single_port}. Max allowed is {MAX_PORT}.")
        args.ports_list = [int(single_port)]
    elif start and end:
        start, end = int(start), int(end)
        if start > end:
            raise ValueError(f"Invalid port range: {args.ports} (start > end)")
        if end > MAX_PORT:
            raise ValueError(f"Invalid port range: {end}. Max allowed is {MAX_PORT}.")
        args.ports_list = list(range(start, end + 1))
    else:
        raise argparse.ArgumentTypeError(f"Invalid port range format: {args.ports}")

    log_msg(f"ARGS PORTS_LIST LENGTH {len(args.ports_list)}", level='DEBUG')
    log_msg(f"ARGS PORTS_LIST START {args.ports_list[0]}", level='DEBUG')
    log_msg(f"ARGS PORTS_LIST END {args.ports_list[-1]}", level='DEBUG')


def init()-> argparse.Namespace:
    """
    Initializes Command-line arguments.

    Accepted arguments:
        -p --port: (str) Ports range 0-65535

    Usage examples: TBD
    """
    log_msg("Initializing Nmap Clone...")
    parser = argparse.ArgumentParser(description='Nmap Clone')

    parser.add_argument('-p', '--ports', required=True, type=str, help="Ports range 0-65535")
    parser.add_argument('-a', '--adresse', required=True, type=str, help="IP- or DNS-Adresse")

    args = parser.parse_args()

    validate_args(args)

    return args