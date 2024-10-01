"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import traceback
from init import init
from logger import log_msg
from utils import extract_metadata, output_doc_info, download_pdfs


def metascan_entrypoint():
    args = init()
    if args.url:
        files = download_pdfs(args.url, args.destination)
    if args.file:
        files = [args.file]
    for file in files:
        doc_info = extract_metadata(file)
        output_doc_info(doc_info, args.destination, args.name)


if __name__ == "__main__":
    try:
        metascan_entrypoint()
    except Exception:
        log_msg(traceback.format_exc(), "ERROR")
