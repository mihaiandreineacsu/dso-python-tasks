# My `hashcat clone` tool

This folder contains the source code for my own implementation of the `hashcat` tool.
**Hashcat** clone can be used to find the plaintext value of a hashed string using various hash functions and attack methods.

This lightweight implementation covers the following features/options:

- Find the plaintext of a hashed string using multiple hash functions.
- Use different attack techniques: Brute-Force or Dictionary Attack.
- Input the hash value either directly or via a file.

## Table of content

- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Command-line arguments](#command-line-arguments)
- [Structure](#structure)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Prove of Concept](#prove-of-concept)

## Technologies

- Windows 11
- Python 3.10.11
- venv (Python virtual environment)

## Dependencies

- exrex==0.11.0: Used to generate all possible combinations of words from a given character set.

## Command-line arguments

### Single Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory | Choices |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--mode` | `-m` | Hash modes: MD5 (0), SHA-1 (1), SHA-256 (2) and SHA-512 (3) | 0 | int | | {0, 1, 2, 3} |
| `--attack` | `-a` | Attack modes: Brute-Force Attack (0) and Dictionary Attack (1) | 0 | int | | {0, 1} |
| `--dictionary` | `-d` | Dictionary file for Dictionary attack | | str | If using Dictionary attack | |
| `--characterset` | `-c` | Character set for Brute-Force attack | `[a-z]{5,5}` | str | | |

### Required Mutual Exclusive Group Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory | Choices |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--hash` | `-h` | Hash provided as direct input | | str | If `--hashfile` not given |  |
| `--hashfile` | `-H` | Hash provided via file | | str | If `--hash` not given |  |

## Structure

- [hashcat.py](./hashcat.py): Main file to run the tool and pass command-line arguments.
- [ini.py](./init.py): Initializes and validates the command-line arguments.
- [utils.py](./utils.py): Contains function definitions used to configure the attack.
- [logger.py](./logger.py): Logs formatted messages.
- [requirements.txt](./requirements.txt): Contains dependencies.

## Getting started

### Installation

```powershell
# Create and activate a Python virtual environment
python -m venv venv
venv/Scripts/activate

# Activate python environment
./venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage examples

```powershell
# Dictionary attack (Direct input of target hash)
python hashcat `
    -m 0 `  # Sets the hash mode to MD5
    -a 1 `  # Sets Dictionary attack mode
    -d somefilecontainingwords.txt `  # Dictionary file is required for Dictionary attack
    -h somehashedtext  # Direct input of the target hash

# Dictionary attack (File input of target hash)
python hashcat `
    -m 1 `  # Sets the hash mode to SHA-1
    -a 1 `  # Sets Dictionary attack mode
    -d somefilecontainingwords.txt `  # Dictionary file is required for Dictionary attack
    -H somefilecontaininghahsedword.txt  # File input of the target hash

# Brute-Force attack (Direct input of target hash)
python hashcat `
    -m 2 `  # Sets the hash mode to SHA-256
    -a 0 ` # Sets Brute-Force attack
    -c '[a-z]{1,3}' `  # Character set used for Brute-Force attack
    -h somehashedtext  # Direct input of the target hash

# Brute-Force attack (File input of target hash)
python hashcat `
    -m 3 `  # Sets the hash mode to SHA-512
    -a 0 `  # Sets Brute-Force attack mode
    -c '[a-z]{1,3}' `  # Character set used for Brute-Force attack
    -H somefilecontaininghahsedword.txt  # File input of the target hash
```

> [!NOTE]
> `--hash` and `--hashfile` are mutually exclusive, and one must be provided.

### Prove of concept

The following examples use Git Bash shell to demonstrate the `hashcat` usage.

#### Brute-force attack

```bash
# Generate and output a SHA-256 hash from the string "weak"
echo -n "weak" | sha256sum | awk '{print $1}'
# Output: 481ba4019c9d2710c3386537382592c093ef02bf5b056c30237b3d92b0e19a1d


# Run hashcat clone
python hashcat.py `
    -m 2 `  # Set hash mode to SHA-256
    -a 0 `  # Set attack mode to Brute-Force
    -c '[a-z]{4,4}' `  # Set character set for Brute-Force attack
    -h  481ba4019c9d2710c3386537382592c093ef02bf5b056c30237b3d92b0e19a1d  # Hash of the string "weak"

[2024-07-15 16:33:39]   [INFO] [Initializing Hashcat Clone...]
[2024-07-15 16:33:39]   [INFO] [Using SHA_256 hash object]
[2024-07-15 16:33:39]   [INFO] [Got 456976 combination(s) to try]
[2024-07-15 16:33:39]   [INFO] [Executing BRUTE_FORCE_ATTACK...]
[2024-07-15 16:33:39]   [INFO] [Execution Lap finished.]
[2024-07-15 16:33:39]   [INFO] [Found match: 481ba4019c9d2710c3386537382592c093ef02bf5b056c30237b3d92b0e19a1d -> weak]
```

#### Dictionary attack

```bash
# Generate and output a SHA-512 hash from the string "power" to hashfile.txt
echo -n "power" | sha512sum | awk '{print $1}' > hashfile.txt
# Output the string "power" to dictionary.txt
echo -n "power" > dictionary.txt


# Run hashcat clone
python hashcat.py `
    -m 3 `  # Set hash mode to SHA-512
    -a 1 `  # Set attack mode to Dictionary
    -d dictionary.txt `  # Dictionary file is required for Dictionary attack
    -H hashfile.txt  # Input the hash from file

[2024-07-15 16:46:51]   [INFO] [Initializing Hashcat Clone...]
[2024-07-15 16:46:51]   [INFO] [Using SHA_512 hash object]
[2024-07-15 16:46:51]   [INFO] [Got 1 combination(s) to try]
[2024-07-15 16:46:51]   [INFO] [Executing DICTIONARY_ATTACK...]
[2024-07-15 16:46:51]   [INFO] [Execution Lap finished.]
[2024-07-15 16:46:51]   [INFO] [Found match: 2fbc66c4dc65497d0215c68eaa88ef90fc19a5562fc7dedd2e177390939a5dbd8604fb377459fb0edb15d85eb3ecc0c01ede4bda708305cf6895428526bc54f1 -> power]
```
