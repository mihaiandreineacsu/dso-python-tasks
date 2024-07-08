
"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from utils import establish_connection, get_words, log_msg


def hydra_entrypoint():
    args = init()
    log_msg(f"Getting words...")
    words = get_words(args)
    log_msg(f"Got {len(words)} Word(s)...")
    log_msg(f"Starting connections to {args.server} as {args.username}\nPlease wait...")
    for index, word in enumerate(words, start=1):
        ssh_client = establish_connection(args, word)
        if ssh_client:
            log_msg(f"Connection {index} established! Password -> {word}\nExecuting command 'whoami'...")
            stdin, stdout, stderr=ssh_client.exec_command("whoami")

            stdout_outlines=stdout.readlines()
            stdout_resp=''.join(stdout_outlines)
            log_msg(f"Command response: {stdout_resp}")

            stderr_outlines=stderr.readlines()
            stderr_resp=''.join(stderr_outlines)
            if stderr_resp:
                log_msg(f"Command error response: {stderr_resp}", "ERROR")

            log_msg("Closing SSH Client...")
            ssh_client.close()
            break
    log_msg("Hydra Exited!")


if __name__ == '__main__':
    hydra_entrypoint()
