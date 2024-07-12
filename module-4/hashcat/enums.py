from enum import Enum
import hashlib
from typing import TypeVar, Generic, List


T = TypeVar('T')

class HashCatEnum(Generic[T]):
    """
    Defines a way to get a list of all values from an Enum Class

    Usage example:
        # Define your Enum Class and inherit HashCatEnum\n
        class MyEnum(HashCatEnum[int], Enum):
            SOME_ENUM = 0
            SOME_OTHER_ENUM = 0


        # Call your Enum Class list will return a list with all of your Enum Class values\n
        MyEnum.list() # [0, 1]
    """

    @classmethod
    def list(cls)-> List[T]:
        return [i.value for i in cls]



class HashModes(HashCatEnum[int], Enum):
    """
    Defines Enums for all supported hash functions.
    """

    MD5 = 0
    SHA_1 = 1
    SHA_256 = 2
    SHA_512 = 3

    @classmethod
    def get_hash_function_map(cls):
        """
        Returns a dictionary as a Map of all defined Enums to a hash function
        """
        return {
            cls.MD5: hashlib.md5,
            cls.SHA_1: hashlib.sha1,
            cls.SHA_256: hashlib.sha256,
            cls.SHA_512: hashlib.sha512,
        }


class AttackModes(HashCatEnum[int], Enum):
    """
    Defines Enums for all supported Attack Modes.
    """
    BRUTE_FORCE_ATTACK = 0
    DICTIONARY_ATTACK = 1

