"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from typing import Any
from scapy.all import IP, TCP, RandShort, sr1, send
from logger import log_msg


def send_rst(dst_ip: str, dst_port: int, src_port: RandShort):
    """
    Send RST to reset the connection (stealthy behavior)
    """
    rst_packet = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="R")
    send(rst_packet, verbose=0)
    log_msg(
        f"Sent RST to {dst_ip}:{dst_port} from port {src_port} to close the connection.",
        "DEBUG",
    )


def send_tcp_package(
    dst_ip: str, dst_port: int, flags: str, src_port=None
) -> tuple[Any, RandShort | int]:
    """
    Sends a TCP packet to a specified destination and returns the response and source port.

    Args:
        dst_ip (str): The destination IP address to send the TCP packet to.
        dst_port (int): The destination port number to send the TCP packet to.
        flags (str): The TCP flags to include in the packet (e.g., "S" for SYN, "A" for ACK).
                     Multiple flags can be combined (e.g., "SA" for SYN-ACK).
        src_port (int, optional): The source port number to use for sending the packet.
        If not provided, a random source port will be generated.

    Returns:
        tuple: A tuple containing:
            - response: The response packet received from the destination, or `None` if no response is received.
            - src_port: The source port number used for sending the packet.

    Example:
        response, src_port = send_tcp_package("192.168.1.1", 80, flags="A")
    """
    if not src_port:
        src_port = RandShort()

    packet = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags=flags)
    response = sr1(packet, timeout=2, verbose=0)
    return response, src_port


def send_package(dst_ip, dst_port):

    # Set up server details
    target_ip = dst_ip
    target_port = dst_port
    source_port = RandShort()  # Random source port
    # Create TCP SYN packet
    syn_packet = IP(dst=target_ip) / TCP(
        sport=source_port, dport=target_port, flags="S"
    )
    syn_ack_response = sr1(syn_packet)
    # Create ACK packet to complete handshake
    ack_packet = IP(dst=target_ip) / TCP(
        sport=syn_ack_response[TCP].dport,
        dport=target_port,
        flags="A",
        seq=syn_ack_response.ack,
        ack=syn_ack_response.seq + 1,
    )
    send(ack_packet)
    # Send some actual data
    data_packet = (
        IP(dst=target_ip)
        / TCP(
            sport=syn_ack_response[TCP].dport,
            dport=target_port,
            flags="PA",
            seq=syn_ack_response.ack,
            ack=syn_ack_response.seq + 1,
        )
        / "Hello from Scapy!"
    )
    send(data_packet)
