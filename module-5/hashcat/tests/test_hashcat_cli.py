import unittest
from unittest.mock import patch
from init import init
from enums import HashModes, AttackModes


class TestHashcatCLI(unittest.TestCase):
    @patch(
        "sys.argv",
        ["hashcat.py", "-m", "0", "-a", "1", "-d", "dictionary.txt", "-h", "somehash"],
    )
    def test_valid_args(self):
        # Test valid arguments where dictionary attack is chosen and hash is provided
        args = init()
        self.assertEqual(args.mode, HashModes.MD5)
        self.assertEqual(args.attack, AttackModes.DICTIONARY_ATTACK)
        self.assertEqual(args.dictionary, "dictionary.txt")
        self.assertEqual(args.hash, "somehash")

    @patch(
        "sys.argv",
        ["hashcat.py", "-m", "1", "-a", "0", "-c", "[0-9]", "-h", "somehash"],
    )
    def test_bruteforce_attack(self):
        # Test Brute-Force attack with character set provided
        args = init()
        self.assertEqual(args.mode, HashModes.SHA_1)
        self.assertEqual(args.attack, AttackModes.BRUTE_FORCE_ATTACK)
        self.assertEqual(args.characterset, "[0-9]")
        self.assertEqual(args.hash, "somehash")

    @patch("sys.argv", ["hashcat.py", "-a", "0", "-h", "somehash"])
    def test_missing_mode(self):
        # Test the case when mode is missing (should default to MD5)
        args = init()
        self.assertEqual(args.mode, HashModes.MD5)
        self.assertEqual(args.attack, AttackModes.BRUTE_FORCE_ATTACK)
        self.assertEqual(args.hash, "somehash")

    @patch(
        "sys.argv",
        ["hashcat.py", "-m", "0", "-a", "1", "-d", "missingfile.txt", "-h", "somehash"],
    )
    def test_missing_dictionary_file(self):
        with self.assertRaises(SystemExit):  # parser.error causes SystemExit
            init()

    @patch("sys.argv", ["hashcat.py", "-m", "0", "-a", "1", "-d", "dictionary.txt", "-H", "hashfile.txt"])
    def test_hashfile_provided(self):
        # Test when the hashfile is provided
        args = init()
        self.assertEqual(args.hashfile, "hashfile.txt")


if __name__ == "__main__":
    unittest.main()
