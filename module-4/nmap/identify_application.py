"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import socket
import time
from logger import log_msg


def identify_application(dst_ip, dst_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        client_socket.connect((dst_ip, dst_port))

        # Send requests based on common protocols
        if dst_port == 80 or dst_port == 8000:
            http_request = (
                f"HEAD / HTTP/1.1\r\nHost: {dst_ip}\r\nConnection: close\r\n\r\n"
            )
            client_socket.sendall(http_request.encode())
        elif dst_port == 21:
            client_socket.sendall(b"USER anonymous\r\n")
        elif dst_port == 25:
            client_socket.sendall(b"HELO example.com\r\n")
        else:
            client_socket.sendall(b"\n")

        time.sleep(2)  # Allow some time for the server to respond

        banner = client_socket.recv(4096)
        log_msg(f"Banner from port {dst_port}: {banner.decode().strip()}", "DEBUG")
        response = banner.decode(errors="ignore")
        # Extract the Server header value
        server_header = None
        for line in response.split("\r\n"):
            if line.lower().startswith("server:"):
                server_header = line
                break

        if server_header:
            log_msg(f"Server header from port {dst_port}: {server_header}")
        else:
            log_msg(f"No Server header found in the response from port {dst_port}.")

        client_socket.close()
    except Exception as e:
        log_msg(f"Failed to identify application on port {dst_port}: {e}")
