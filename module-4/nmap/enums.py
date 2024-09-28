"""
This script is intended solely for educational purposes as an exercise in imitation.
Any practical use of this script outside of educational or supervised demonstration scenarios is strictly prohibited.

Author: Mihai-Andrei Neacsu
"""

from enum import Enum
from typing import Type, TypeVar, Generic, List

T = TypeVar("T")


class NmapEnum(Generic[T]):
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
    def list(cls: Type["NmapEnum[T]"]) -> List[T]:
        return [i.value for i in cls]


class RangeEnum(NmapEnum[int], Enum):
    MAX_PORT = 65535
    MIN_PORT = 0


class FlagsEnum(NmapEnum[int], Enum):
    MAX_PORT = 65535
    MIN_PORT = 0
    FIN = 0x01  # Finish (Close the connection)
    SYN = 0x02  # Synchronize (Initiate a connection)
    RST = 0x04  # Reset (Abort the connection)
    PSH = 0x08  # Push (Push buffered data to the application)
    ACK = 0x10  # Acknowledgment (Acknowledge receipt of data)
    URG = 0x20  # Urgent (Data is urgent)
    ECE = 0x40  # ECN-Echo (Explicit Congestion Notification)
    CWR = 0x80  # Congestion Window Reduced
    NS = 0x100  # Nonce Sum (Experimental)

    @classmethod
    def combine_flags(cls, *flags):
        """
        Combine specified TCP flags into a single value.

        Args:
            *flags: Any number of FlagsEnum members to combine.

        Returns:
            A hexadecimal string representing the combined value of the specified flags.
        """
        combined_value = 0

        for flag in flags:
            combined_value |= flag.value

        return hex(combined_value)
