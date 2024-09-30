"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from init import init
from logger import log_msg
from utils import extract_metadata, output_doc_info


def mdpdf_entrypoint():
    args = init()
    doc_info = extract_metadata(args.file)
    output_doc_info(doc_info, args.destination, args.name)


if __name__ == "__main__":
    try:
        mdpdf_entrypoint()
    except Exception as e:
        log_msg(f"{e}", "ERROR")
