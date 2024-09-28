"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from threading import Thread
from logger import log_msg
import argparse
from scans import (
    half_open_scan,
    os_fingerprint,
    ping_scan,
    tcp_ack_scan,
    tcp_connect_scan,
    tcp_fin_scan,
    tcp_null_scan,
    tcp_window_scan,
    tcp_xmas_scan,
)


def is_port_opened(dst_ip: str, dst_port: int) -> bool:
    """
    Scans a specified destination port if is opened using TCP scan technics.

    Args:
        dst_ip (str):   The destination IP address to send the TCP packet to.
        dst_port (int): The destination port number to send the TCP packet to.

    Returns:
        True:   If any TCP scan result is "Open"
        False:  If Ping scan result is not "Alive" or
                TCP scans result is not "Unfiltered", "Closed" or
                All scans exhausted
    """
    result = ping_scan(dst_ip)
    if result != "Alive":
        return False
    result = tcp_ack_scan(dst_ip, dst_port)
    if result != "Unfiltered":
        return False
    result = half_open_scan(dst_ip, dst_port)
    if result == "Open":
        return True
    result = tcp_window_scan(dst_ip, dst_port)
    if result == "Open":
        return True
    result = tcp_connect_scan(dst_ip, dst_port)
    if result == "Open":
        return True
    result = tcp_null_scan(dst_ip, dst_port)
    if result == "Closed":
        return False
    result = tcp_xmas_scan(dst_ip, dst_port)
    if result == "Closed":
        return False
    result = tcp_fin_scan(dst_ip, dst_port)
    if result == "Closed":
        return False
    return False


def scan_port(dst_ip: str, dst_port: int, os_scan: bool = False):
    """
    Scans a specified destination port if is opened.
    If the destination port is opened and os_scan flag is on, os_fingerprint scan will run

    Args:
        dst_ip (str): The destination IP address to send the TCP packet to.
        dst_port (int): The destination port number to send the TCP packet to.
    """
    is_open = is_port_opened(dst_ip, dst_port)
    if is_open and os_scan:
        os_info = os_fingerprint(dst_ip, dst_port)
        if os_info["OS"]:
            log_msg(f"OS: {os_info['OS']}")


def find_opened_ports(args: argparse.Namespace):
    """
    Scans the given address for each port in ports list.
    Each scan starts in a Thread.
    """
    log_msg("Finding opened ports ...")
    for port in args.ports_list:
        address = args.address
        thread = Thread(target=scan_port, args=(address, port, True))
        thread.start()
