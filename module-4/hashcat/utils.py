"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

import argparse
from enums import AttackModes, HashModes
import exrex
from logger import log_msg


def get_target_hash(args: argparse.Namespace) -> str:
    """
    Get the target hash from the Command-line arguments:
        - direct from args.hash if its set
        - form a file containing the hash if args.hashfile is set

    Args:
        args (argparse.Namespace): Passed args on script run

    Returns:
        str : target hash
    """
    if args.hash:
        return args.hash
    if args.hashfile:
        with open(args.hashfile, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            return first_line


def get_hash_obj(args: argparse.Namespace):
    """
    Get the hash object based on chosen hash mode

    Args:
        args (argparse.Namespace): Passed args on script run

    Returns:
        _Hash : hash object
    """
    hash_function = HashModes.get_hash_function_map()[args.mode]
    hash_obj = hash_function()
    return hash_obj


def get_words_from_dictionary(args: argparse.Namespace) -> list[str]:
    """
    Get the words list from a dictionary file if Dictionary Attack is chosen

    Args:
        args (argparse.Namespace): Passed args on script run

    Returns:
        list[str] : words list
    """
    with open(args.dictionary, "r", encoding="utf-8") as file:
        words = file.read().splitlines()
        log_msg(f"Got {len(words)} combination(s) to try")
        return words


def get_words_from_character_set(args: argparse.Namespace) -> list[str]:
    """
    Get the words list from a character set for a Brute-Force Attack

    Args:
        args (argparse.Namespace): Passed args on script run

    Returns:
        list[str] : words list
    """
    log_msg(f"Got {exrex.count(args.characterset)} combination(s) to try")
    words = exrex.generate(args.characterset)
    return words


def get_words(args: argparse.Namespace) -> list[str]:
    """
    Based on provided Command-line arguments, it will:
        - get the words list from a dictionary file if Dictionary Attack is chosen
        - get the words list from a character set if Brute-Force Attack is chosen

    Args:
        args (argparse.Namespace): Passed args on script run

    Returns:
        list[str] : words list
    """
    if args.attack == AttackModes.DICTIONARY_ATTACK:
        words = get_words_from_dictionary(args)
    if args.attack == AttackModes.BRUTE_FORCE_ATTACK:
        words = get_words_from_character_set(args)
    return words


def exec_attack(args: argparse.Namespace):
    """
    Based on provided Command-line arguments, it will:
        1. get the right hash object, used to hash a word
        1. get the target hash from Command-line arguments
        1. get the words list, used to check against the target hash
        1. for each word, hashes it with the chosen hash object
        1. check the hashed word if it matches the target hash

    Args:
        args (argparse.Namespace): Passed args on script run
    """
    log_msg(f"Using {args.mode.name} hash object")
    target_hash = get_target_hash(args)
    words = get_words(args)
    log_msg(f"Executing {args.attack.name}...")
    try:
        for word in words:
            hash_obj = get_hash_obj(args)
            hash_obj.update(word.encode())
            hash = hash_obj.hexdigest()
            if target_hash == hash:
                log_msg("Execution Lap finished.")
                log_msg(f"Found match: {target_hash} -> {word}")
                return
    except KeyboardInterrupt:
        log_msg(f"Execution Lap interrupted at {hash} -> {word}")
        return
    log_msg("Execution Lap finished.")
    log_msg("No match cloud be found!")
