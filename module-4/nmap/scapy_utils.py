"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import time
from typing import Any
from scapy.all import IP, TCP, RandShort, sr1, send, ICMP
from logger import log_msg
from literals import (
    PingScanResult,
    TcpAckScanResult,
    HalfOpenScanResult,
    TcpConnectScanResult,
    TcpFinScan,
    TcpWindowScanResult,
    TcpNullScanResult,
    TcpXmasScanResult,
)


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


def ping_scan(
    dst_ip: str,
) -> PingScanResult:
    """
    Perform a Ping Scan on the specified IP address.

    Args:
        dst_ip (str): The target IP address.

    Returns:
        PingScanResult: The state of the host.
    """
    # Step 1: Send an ICMP Echo Request to the target IP
    icmp_packet = IP(dst=dst_ip) / ICMP()
    response = sr1(icmp_packet, timeout=2, verbose=0)

    # Step 2: Analyze the response
    if response is None:
        log_msg(f"Host {dst_ip}: Down or Filtered", "DEBUG")
        return "Down or Filtered"

    if response.haslayer(ICMP):
        icmp_layer = response.getlayer(ICMP)

        if icmp_layer.type == 0:  # ICMP Echo Reply received
            log_msg(f"Host {dst_ip}: Alive", "DEBUG")
            return "Alive"
    log_msg(f"Host {dst_ip}: Unexpected Response", "DEBUG")
    return "Unexpected Response"


def tcp_ack_scan(dst_ip: str, dst_port: int) -> TcpAckScanResult:
    """
    Perform a TCP ACK Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        TcpAckScanResult : The state of the host.
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="A")

    if response is None:
        log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or No Response", "DEBUG")
        return "Filtered or No Response"

    if response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x04:  # RST received, port is unfiltered
            log_msg(f"Host {dst_ip} Port {dst_port}: Unfiltered", "DEBUG")
            return "Unfiltered"

    if response.haslayer(ICMP):
        icmp_layer = response.getlayer(ICMP)
        if int(icmp_layer.type) == 3 and int(icmp_layer.code) in [1, 2, 3, 9, 10, 13]:
            log_msg(f"Host {dst_ip} Port {dst_port}: Filtered", "DEBUG")
            return "Filtered"

    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


def half_open_scan(dst_ip: str, dst_port: int) -> HalfOpenScanResult:
    """
    Perform a Half-Open Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        HalfOpenScanResult : The state of the host.
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="A")
    if not response:
        log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Dropped", "DEBUG")
        return "Filtered or Dropped"
    if not response.haslayer(TCP):
        log_msg(f"Host {dst_ip} Port {dst_port}: Unexpected TCP Flags", "DEBUG")
        return "Unexpected TCP Flags"
    log_msg(f"TCP Layer flags: {response.getlayer(TCP).flags}", "DEBUG")
    if response.getlayer(TCP).flags == 0x14:  # RST+ACK
        log_msg(f"Host {dst_ip} Port {dst_port}: Closed", "DEBUG")
        return "Closed"
    if response.getlayer(TCP).flags == 0x12:  # SYN+ACK
        log_msg(f"Host {dst_ip} Port {dst_port}: Open")
        time.sleep(2)
        send_rst(dst_ip, dst_port, src_port)
        return "Open"
    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


def tcp_window_scan(dst_ip: str, dst_port: int) -> TcpWindowScanResult:
    """
    Perform a TCP Window Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        TcpWindowScanResult : The state of the port.
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="A")

    if response is None:
        log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or No response", "DEBUG")
        return "Filtered or No response"  # No response indicates the port might be filtered or dropped

    if response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x04:  # RST received
            log_msg(f"tcp_layer.window {tcp_layer.window}", "DEBUG")
            if tcp_layer.window > 0:  # Non-zero window size
                log_msg(f"Host {dst_ip} Port {dst_port}: Open")
                return "Open"
            else:  # Zero window size
                log_msg(f"Host {dst_ip} Port {dst_port}: Closed", "DEBUG")
                return "Closed"
    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


def tcp_connect_scan(dst_ip: str, dst_port: int) -> TcpConnectScanResult:
    """
    Perform a TCP Connect Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        TcpConnectScanResult : The state of the port
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="S")

    if response is None:
        log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Dropped", "DEBUG")
        return "Filtered or Dropped"

    if response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x12:  # SYN-ACK received, port is open
            # Send an ACK packet to complete the handshake
            ack_packet = IP(dst=dst_ip) / TCP(
                sport=src_port,
                dport=dst_port,
                flags="A",
                seq=response.ack,
                ack=tcp_layer.seq + 1,
            )
            send(ack_packet, verbose=0)

            # Optional: Send an RST packet to close the connection
            rst_packet = IP(dst=dst_ip) / TCP(
                sport=src_port,
                dport=dst_port,
                flags="R",
                seq=response.ack,
                ack=tcp_layer.seq + 1,
            )
            send(rst_packet, verbose=0)

            log_msg(f"Host {dst_ip} Port {dst_port}: Open")
            return "Open"

        elif tcp_layer.flags == 0x14:  # RST-ACK received, port is closed
            log_msg(f"Host {dst_ip} Port {dst_port}: Closed", "DEBUG")
            return "Closed"

    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


def tcp_null_scan(dst_ip: str, dst_port: int) -> TcpNullScanResult:
    """
    Perform a TCP NULL Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        TcpNullScanResult : The state of the port.
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="")

    if response is None:
        log_msg(f"Host {dst_ip} Port {dst_port}: Open or Filtered", "DEBUG")
        return "Open or Filtered"

    if response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x14:  # RST-ACK received, port is closed
            log_msg(f"Host {dst_ip} Port {dst_port}: Closed", "DEBUG")
            return "Closed"

    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


def tcp_xmas_scan(dst_ip: str, dst_port: int) -> TcpXmasScanResult:
    """
    Perform a TCP XMAS Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        TcpXmasScanResult : The state of the port.
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="FPU")

    if response is None:
        log_msg(f"Host {dst_ip} Port {dst_port}: Open or Filtered", "DEBUG")
        return "Open or Filtered"

    if response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x14:  # RST-ACK received, port is closed
            log_msg(f"Host {dst_ip} Port {dst_port}: Closed", "DEBUG")
            return "Closed"

    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


def tcp_fin_scan(dst_ip: str, dst_port: int) -> TcpFinScan:
    """
    Perform a TCP FIN Scan on the specified port.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number.

    Returns:
        TcpFinScan : The state of the port.
    """
    response, src_port = send_tcp_package(dst_ip, dst_port, flags="F")

    # Step 2: Analyze the response
    if response is None:
        log_msg(f"Host {dst_ip} Port {dst_port}: Open or Filtered", "DEBUG")
        return "Open or Filtered"

    if response.haslayer(TCP):
        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x14:  # RST-ACK received, port is closed
            log_msg(f"Host {dst_ip} Port {dst_port}: Closed", "DEBUG")
            return "Closed"

    log_msg(f"Host {dst_ip} Port {dst_port}: Filtered or Unexpected Response", "DEBUG")
    return "Filtered or Unexpected Response"


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


def os_fingerprint(dst_ip: str, dst_port: int) -> dict:
    """
    Perform a basic OS fingerprinting scan by analyzing the TTL and TCP window size.

    Args:
        dst_ip (str): The target IP address.
        dst_port (int): The target port number (should be open).

    Returns:
        dict: A dictionary containing the inferred OS characteristics.
    """
    os_info = {}

    # Step 1: Send a SYN packet to the target IP and port
    syn_packet = IP(dst=dst_ip) / TCP(dport=dst_port, flags="S")
    response = sr1(syn_packet, timeout=2, verbose=0)

    # Step 2: Analyze the response
    if response is None:
        os_info["OS"] = "No response (Host might be down or filtered)"
        return os_info

    if response.haslayer(IP) and response.haslayer(TCP):
        ip_layer = response.getlayer(IP)
        tcp_layer = response.getlayer(TCP)

        # Analyze TTL (Time to Live)
        ttl = ip_layer.ttl
        if ttl <= 64:
            os_info["TTL"] = ttl
            os_info["OS"] = "Linux/Unix"
        elif ttl <= 128:
            os_info["TTL"] = ttl
            os_info["OS"] = "Windows"
        elif ttl <= 255:
            os_info["TTL"] = ttl
            os_info["OS"] = "Cisco or Solaris"

        # Analyze TCP Window Size
        window_size = tcp_layer.window
        os_info["TCP Window Size"] = window_size
        if window_size == 5840:
            os_info["OS"] += " (Linux)"
        elif window_size == 8192:
            os_info["OS"] += " (Windows XP/2000)"
        elif window_size == 65535:
            os_info["OS"] += " (Windows 7/Server 2008 R2)"
        else:
            os_info["OS"] += " (Unknown OS)"
    return os_info


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
