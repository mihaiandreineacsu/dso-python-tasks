"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
from logger import init_logger, log_msg
import re
import enums


def validate_port_range(
    ports: str,
) -> tuple[str | None, str | None, str | None, str | None]:
    """
    Validates given ports range format using a regex expression
    and returns the matched groups.

    Accepted formats:
        - One number from 1 to maximal 5 digits (\\d{1,5}).
            Ex.: 8, 22, 443, 5000, 65535
        - Two numbers from 1 to maximal 5 digits separated by a hyphen (\\d{1,5})-(\\d{1,5}).
            Ex.: 22-2222
        - A hyphen (-)

    Args:
        ports (str): Ports format to validate.

    Raises:
        argparse.ArgumentTypeError: If validation fails.

    Returns:
        tuple : Matched groups: start, end, single_port, hyphen

    """
    log_msg(f"PORTS Range: {ports}", level="DEBUG")
    port_range_regex = re.compile(r"^(?:(\d{1,5})-(\d{1,5})|(\d{1,5})|(-))$")
    match = port_range_regex.match(ports)
    if not match:
        raise argparse.ArgumentTypeError(f"Invalid port range format: {ports}")
    return match.groups()


def validate_ports_list(
    start: str, end: str, single_port: str, hyphen: str, ports: str
) -> list[int]:
    """
    Validates ports list by given start and end ports or single port or hyphen:
        - If hyphen is defined returns list range of ports from 0 to (MAX_PORT + 1) value.
        - Else if single_port is defined but not greater then MAX_PORT,
          a list of one element containing single_port value is returned.
        - Else if start and end ports are defined but start port not greater then end
          and end not greater then MAX_PORT
          a list range of port from start port value to end port value + 1 is returned.

    Args:
        start (str) : starting port
        end (str) : ending port
        single_port (str): single port value
        ports (str): original ports format

    Returns:
        list[int] : A list of ports numbers.
        Possible outcomes:
            - [0, MAX_PORT + 1]
            - [start, end + 1]
            - [single_port]

    Raises:
        ValueError:
            - If single_port greater then MAX_PORT
            - If start is greater then end and end greater then MAX_PORT
        argparse.ArgumentTypeError: If no list of ports could be created from the given values.
    """
    MAX_PORT = enums.RangeEnum.MAX_PORT.value
    if hyphen:
        ports_list = list(range(MAX_PORT + 1))
    elif single_port:
        single_port = int(single_port)
        if single_port > MAX_PORT:
            raise ValueError(f"Invalid port: {single_port}. Max allowed is {MAX_PORT}.")
        ports_list = [int(single_port)]
    elif start and end:
        start, end = int(start), int(end)
        if start > end:
            raise ValueError(
                f"Invalid port range: Start port {start} can be greater then end port {end}"
            )
        if end > MAX_PORT:
            raise ValueError(f"Invalid port range: {end}. Max allowed is {MAX_PORT}.")
        ports_list = list(range(start, end + 1))
    else:
        raise argparse.ArgumentTypeError(f"Invalid port range format: {ports}")
    return ports_list


def validate_args(args: argparse.Namespace):
    """
    Validates Command-Line arguments.
        1. validates given ports range format
        1. validates ports list range
    """
    start, end, single_port, hyphen = validate_port_range(args.ports)

    log_msg(f"Start PORT {start}", level="DEBUG")
    log_msg(f"End PORT {end}", level="DEBUG")
    log_msg(f"Single PORT {single_port}", level="DEBUG")
    log_msg(f"Hyphen {hyphen}", level="DEBUG")

    args.ports_list = validate_ports_list(start, end, single_port, hyphen, args.ports)

    log_msg(f"ARGS PORTS_LIST LENGTH {len(args.ports_list)}", "DEBUG")
    log_msg(f"ARGS PORTS_LIST START {args.ports_list[0]}", "DEBUG")
    log_msg(f"ARGS PORTS_LIST END {args.ports_list[-1]}", "DEBUG")


def init() -> argparse.Namespace:
    """
    Initializes Command-line arguments.

    Accepted arguments:
        -p --ports: (str) Ports range 0-65535
        -a --address: (str) IP- or DNS-Address
        -d --debug: (bool) Prints debug logs

    Usage examples: TBD
    """
    parser = argparse.ArgumentParser(description="Nmap Clone")

    parser.add_argument(
        "-p", "--ports", required=True, type=str, help="Ports range 0-65535"
    )
    parser.add_argument(
        "-a", "--address", required=True, type=str, help="IP- or DNS-Address"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Prints debug logs")

    args = parser.parse_args()
    init_logger(args)
    log_msg("Initializing Nmap Clone...")
    validate_args(args)

    return args
