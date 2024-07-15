import unittest
import subprocess


class BruteForceTests(unittest.TestCase):

    def test_brute_force__sha256(self):
        pass
        # subprocess.call("echo -n 'weak' | sha256sum | awk '{print $1}'")
        # output = subprocess.check_output(['echo', '-n'])
        # print(output)


if __name__ == '__main__':
    unittest.main()