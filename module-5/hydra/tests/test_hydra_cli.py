import unittest
from unittest.mock import patch
from init import init


class TestHydraCLI(unittest.TestCase):

    @patch(
        "sys.argv",
        ["hydra.py", "-u", "username", "-s", "servername", "-p", "22", "-w", "dictionary.txt"],
    )
    def test_valid_args(self):
        # Test valid arguments where dictionary attack is chosen and hash is provided
        args = init()
        self.assertEqual(args.username, "username")
        self.assertEqual(args.server, "servername")
        self.assertEqual(args.port, 22)
        self.assertEqual(args.wordlist, "dictionary.txt")


if __name__ == "__main__":
    unittest.main()
