"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from scapy_utils import scan_port
from threading import Thread
from logger import log_msg
import argparse


def find_opened_ports(args: argparse.Namespace):
    """
    Scanes the given adresse for each port in ports list.
    Each scan starts in a Thread.
    """
    log_msg("Finding opened ports ...")
    for port in args.ports_list:
        adresse = args.adresse
        thread = Thread(target=scan_port, args=(adresse, port, True))
        thread.start()
