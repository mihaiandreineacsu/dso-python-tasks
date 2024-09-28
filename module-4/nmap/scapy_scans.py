def half_open_scan():
    """
    TCP SYN Scan (Half-Open Scan):
    Description: A TCP SYN scan sends a SYN packet to the target port and waits for a response.
    If the target replies with a SYN-ACK, the port is considered open
    and the scanner immediately sends an RST (Reset) packet to avoid completing the TCP handshake.
    This is why it's often called a "half-open" scan.
    Use Case: It's one of the most popular scan types because it's fast and stealthy.
    It doesn't complete the three-way handshake, which can avoid logging on some systems.
    Typical Response:
    SYN-ACK: Port is open.
    RST: Port is closed.
    No response or ICMP unreachable: Port is filtered.
    """
