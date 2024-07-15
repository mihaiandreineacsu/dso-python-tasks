# My `hash clone` tool

This folder contains the source code for my own implementation of the `hydra` tool.
Hash clone can be used to TBD.

This is a lightweight implementation that covers the following features/options:

- ...
- ...

## Table of content

- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Command-line arguments](#command-line-arguments)
- [Structure](#structure)
- [Getting started](#getting-started)
- [Installation](#installation)
- [Usage examples](#usage-examples)
- [Prove of concept](#prove-of-concept)

## Technologies

- Windows 11
- Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
- venv (python virtual environment)

## Dependencies

- exrex==0.11.0: used to generate all possible combinations of words from give characterset command-line argument

## Command-line arguments

### Single Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory | Choices |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--mode` | `-m` | Hashmodes MD5 (0), SHA-1 (1), SHA-256 (2) and SHA-512 (3) | 0 | int | | {0, 1, 2, 3} |
| `--attack` | `-a` | Attack modes Brute-Force Attack (0) and Dictionary Attack (1) | 0 | int | | {0, 1} |
| `--dictionary` | `-d` | Dictionary file for Dictionary attack | | str | If Dictionary Attack is chosen | |
| `--characterset` | `-c` | Character set for Brute-Force attack | [a-z]{5,5} | str | | |

### Required Mutual exclusive Group Command-line arguments

| Name | Shortname | Description | Default | Type | Mandatory | Choices |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `--hash` | `-h` | Hash from direct input | | str | If hashfile not given |  |
| `--hashfile` | `-H` | Hash from file | | str | If hash not given |  |

## Structure

- [hashcat.py](./hashcat.py): Main file to run and pass command-line arguments
- [ini.py](./init.py): initializes and validates the command-line arguments
- [utils.py](./utils.py): functions definitions used to configure the attack
- [logger.py](./logger.py): Logs formatted messages
- [requirements.txt](./requirements.txt): contains dependencies

## Getting started

### Installation

```powershell
# Create and activate python virtual environment
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
python hashcat \
    -m 0 \ # Sets the hash mode to MD5 (You can choose a different one, See Command-line arguments Table)
    -a 1 \ # Sets Dictionary attack
    -d somefilecontainingwords.txt \ # this is mandatory for Dictionary attack
    -h somehashedtext # Direct input of target hash

# Dictionary attack (File input of target hash)
python hashcat \
    -m 1 \ # Sets the hash mode to SHA-1 (You can choose a different one, See Command-line arguments Table)
    -a 1 \ # Sets Dictionary attack
    -d somefilecontainingwords.txt \ # this is mandatory for Dictionary attack
    -H somefilecontaininghahsedword.txt # File input of target hash

# Brute-Force attack (Direct input of target hash)
python hashcat \
    -m 2 \ # Sets the hash mode to SHA-256 (You can choose a different one, See Command-line arguments Table)
    -a 0 \ # Sets Brute-Force attack
    -c '[a-z]{1,3}' \ # Character set used for Brute-Force attack
    -h somehashedtext # Direct input of target hash

# Brute-Force attack (File input of target hash)
python hashcat \
    -m 3 \ # Sets the hash mode to SHA-512 (You can choose a different one, See Command-line arguments Table)
    -a 0 \ # Sets Brute-Force attack
    -c '[a-z]{1,3}' \ # Character set used for Brute-Force attack
    -H somefilecontaininghahsedword.txt # File input of target hash
```

> [!NOTE]
> `--hash` and `--hashfile` are mutual exclusive, and at least one musst be given.

### Prove of concept

The example that follows uses git bash shell for an easy way of demonstrating hashcat usage.

#### Brute-force attack

```bash
# Generate and outputs a hash from string "weak"
echo -n "weak" | sha256sum | awk '{print $1}'
481ba4019c9d2710c3386537382592c093ef02bf5b056c30237b3d92b0e19a1d

# Run hashcat
python hashcat.py \
    -m 2 \ # set hashmode to SHA-256
    -a 0 \ # set attack mode to Brute-Force
    -c '[a-z]{4,4}' \ # set characterset for Brute-Force attach
    -h  481ba4019c9d2710c3386537382592c093ef02bf5b056c30237b3d92b0e19a1d # SHA-256 hash value of string "weak"

[2024-07-15 16:33:39]   [INFO] [Initializing Hashcat Clone...]
[2024-07-15 16:33:39]   [INFO] [Using SHA_256 hash object]
[2024-07-15 16:33:39]   [INFO] [Got 456976 combination(s) to try]
[2024-07-15 16:33:39]   [INFO] [Executing BRUTE_FORCE_ATTACK...]
[2024-07-15 16:33:39]   [INFO] [Execution Lap finished.]
[2024-07-15 16:33:39]   [INFO] [Found match: 481ba4019c9d2710c3386537382592c093ef02bf5b056c30237b3d92b0e19a1d -> weak]
```

#### Dictionary attack

```bash
# Generate and outputs a hash from string "power" to hashfile.txt file
echo -n "power" | sha512sum | awk '{print $1}' > hashfile.txt
# Outputs the string "power" to dictionary.txt
echo -n "power" > dictionary.txt

# Run hashcat
python hashcat.py \
    -m 3 \ # set hashmode to SHA-512
    -a 1 \ # set attack mode to Dictionary attack
    -d dictionary.txt \ # set dictionary file for Dictionary attack to use
    -H hashfile.txt # set hashfile to read the SHA-512 hash value of string "power" from

[2024-07-15 16:46:51]   [INFO] [Initializing Hashcat Clone...]
[2024-07-15 16:46:51]   [INFO] [Using SHA_512 hash object]
[2024-07-15 16:46:51]   [INFO] [Got 1 combination(s) to try]
[2024-07-15 16:46:51]   [INFO] [Executing DICTIONARY_ATTACK...]
[2024-07-15 16:46:51]   [INFO] [Execution Lap finished.]
[2024-07-15 16:46:51]   [INFO] [Found match: 2fbc66c4dc65497d0215c68eaa88ef90fc19a5562fc7dedd2e177390939a5dbd8604fb377459fb0edb15d85eb3ecc0c01ede4bda708305cf6895428526bc54f1 -> power]
```
