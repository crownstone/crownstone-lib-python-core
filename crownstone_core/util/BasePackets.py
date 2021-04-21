"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in ExampleBasePackets.py
"""

from enum import IntEnum
from crownstone_core.util.Conversion import Conversion

class PacketBase:
    def getPacket(self):
        """
        Serializes the whole object by calling getPacket on each member variable and
        appending the return values to a list.
        """
        packet = []
        for name, val in self.__dict__.items():
            packet += val.getPacket()
        return packet

    def __setattr__(self, name, value):
        """
        Enforces type equality after assignment
        """
        if name in self.__dict__:
            t = type(self.__dict__[name])
            if t is not type(value):
                # try to cast value to the correct type.
                value = t(value)
        self.__dict__[name] = value

    def __str__(self):
        return "{0}({1})".format(
            type(self).__name__,
            ", ".join([f"{k}: {str(v)}" for k, v in self.__dict__.items()])
        )


# ----- common int packet details -----


class IntPacket(PacketBase):
    """
    Used as base class for the integers to support common operations among them and
    enable explicit cast to int.
    Subclasses are required to contain a field with the name 'val'.
    """
    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return self.val != other.val

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self.val <= other.val

    def __gt__(self, other):
        return self.val > other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __int__(self):
        return self.val


# ----- literal types -------
class Uint8(IntPacket):
    def __init__(self, val=0):
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint8_to_uint8_array(self.val)

    def __str__(self):
        return f"{str(self.val)}"


class Uint16(IntPacket):
    def __init__(self, val=0):
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint16_to_uint8_array(self.val)

    def __str__(self):
        return f"{str(self.val)}"


class Uint8Array(PacketBase):
    def __init__(self, val=[]):
        self.val = list([int(x) for x in val])

    def getPacket(self):
        return self.val

    def __str__(self):
        return f"{str(self.val)}"


class Uint16Array(PacketBase):
    def __init__(self, val=[]):
        self.val = list([int(x) for x in val])

    def getPacket(self):
        return Conversion.uint16_array_to_uint8_array(self.val)

    def __str__(self):
        return f"{str(self.val)}"

class PacketBaseList(PacketBase):
    """
    Wraps a generic list of descendants of PacketBase and packs them individually.
    Providing a cls parameter gives a type hint.
    """
    def __init__(self, cls=None, val=[]):
        if cls is None:
            raise ValueError("cls is required")
        if type(cls) is not type:
            raise ValueError("cls must be a type object")
        if not issubclass(cls, PacketBase):
            raise ValueError("cls must be a type object subclassing PacketBase")
        # try to cast value to the correct type if that wasn't the case yet.
        self.val = [value if type(value) is cls else cls(value) for value in val]

    def getPacket(self):
        packet = []
        for name, val in self.val:
            packet += val.getPacket()
        return packet


class CsUint8Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint8_to_uint8_array(int(self))


class CsUint16Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(int(self))