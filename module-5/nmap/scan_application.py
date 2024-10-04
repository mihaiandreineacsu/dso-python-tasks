"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from functools import wraps
import socket
import time
from logger import log_msg

# Sample mapping of known banners to applications
BANNER_SIGNATURES = {
    "nginx": "Nginx Web Server",
    "apache": "Apache HTTP Server",
    "IIS": "Microsoft IIS Server",
    "Postfix": "Postfix Mail Server",
    "Exim": "Exim Mail Server",
    "OpenSSH": "OpenSSH Server",
    "vsftpd": "vsftpd FTP Server",
    "ProFTPD": "ProFTPD FTP Server",
    "SMTP": "SMTP Server",
    # Add more known banners and applications here
}

PROB_MESSAGES = [
    b"\n",
    b"HEAD / HTTP/1.1\r\n\r\n",
    b"SSH-2.0-OpenSSH\r\n",
    b"HELO example.com\r\n",
]


# Decorator to retry on timeout and change the probe message
def retry_on_timeout(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(dst_ip, dst_port, *args, **kwargs):

            retries = 0
            while retries < max_retries:
                try:
                    # Use the retry number to select a probe message
                    probe_message = (
                        PROB_MESSAGES[retries]
                        if retries < len(PROB_MESSAGES)
                        else b"\n"
                    )
                    return func(dst_ip, dst_port, probe_message, *args, **kwargs)
                except socket.timeout:
                    retries += 1
                    log_msg(
                        f"Timeout on port {dst_port}, retrying... ({max_retries - retries} retries left)",
                        "WARNING",
                    )
                except Exception as e:
                    log_msg(f"Failed on port {dst_port}: {e}", "ERROR")
                    break
            log_msg(
                f"Max retries reached on port {dst_port}. Could not identify the application.",
                "ERROR",
            )

        return wrapper

    return decorator


def match_application_signature(banner: str) -> str | None:
    """
    Match the banner against known signatures to identify the application.

    Args:
        banner (str) : received decoded banner from send probe message
    """
    for signature, app_name in BANNER_SIGNATURES.items():
        if signature.lower() in banner.lower():
            return app_name
    return None  # No match found


# Decorated function to scan for applications
@retry_on_timeout(max_retries=2)
def scan_application(dst_ip: str, dst_port: str, probe_message: bytes = b"\n"):
    """
    Identifies application listening on given address and port.

    Args:
        dst_ip (str) : Target Address
        dst_port (str) : Target port
        probe_message (bytes) : Message to send via client socket
        A newline (b"\n") is often sufficient to trigger a banner
    """

    log_msg("Scanning APPLICATION...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(3)
    client_socket.connect((dst_ip, dst_port))

    # Send a generic message to probe the service
    client_socket.sendall(probe_message)

    time.sleep(2)  # Allow some time for the server to respond

    banner = client_socket.recv(4096)
    log_msg(f"Banner from port {dst_port}: {banner.decode().strip()}", "DEBUG")

    response = banner.decode(errors="ignore")

    # Try to match the banner to a known application
    detected_application = match_application_signature(response)
    if detected_application:
        log_msg(f"Port {dst_port} runs: {detected_application} APPLICATION")
    else:
        log_msg(
            f"Could not identify the application from the banner on port {dst_port}."
        )

    client_socket.close()
