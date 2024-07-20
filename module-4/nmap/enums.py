"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from enum import Enum
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


class RangeEnum(HashCatEnum[int], Enum):
    MAX_PORT = 65535
    MIN_PORT = 0