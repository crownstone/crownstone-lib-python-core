"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in ExampleBasePackets.py
"""

from enum import IntEnum

from crownstone_core.util.BufferReader import BufferReader

from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.Bitmasks import Bitmasks

class PacketBase:
    def getPacket(self):
        """
        Serializes the whole object by calling getPacket on each member variable and
        appending the return values to a list of uint8s .
        """
        packet = []
        for name, val in self.__dict__.items():
            packet += val.getPacket()
        return packet

    def setPacket(self, bytelist):
        """
        Loads the object from the given bytelist, returning the tail of the bytelist
        consisting of all bytes that weren't used by this setPacket call.

        Failure to setPacket invocations are required to throw an exception of type ValueError.
        """
        for name, val in self.__dict__.items():
            bytelist = self.__dict__[name].setPacket(bytelist)
        return bytelist


    def __setattr__(self, name, value):
        """
        Enforces type equality after assignment.
        """
        if name in self.__dict__:
            t = type(self.__dict__[name])
            if t is not type(value):
                # try to cast value to the correct type.
                value = t(value)
        self.__dict__[name] = value

    def __repr__(self):
        return "{0}({1})".format(
            type(self).__name__,
            ", ".join([f"{k}: {str(v)}" for k, v in self.__dict__.items()])
        )

    def fromData(self, data: [int]):
        """
        This will fill all the fields back from a data array. Is more or less the inverse of the getPacket.
        The main difference is that arrays will throw an error if you have not defined a size.
        """
        reader = BufferReader(data)

        for name, value in self.__dict__.items():
            t = value.__class__.__name__
            if t == "Uint8":
                value.val = reader.getUInt8()
            elif t == "Int8":
                value.val = reader.getInt8()
            elif t == "Uint16":
                value.val = reader.getUInt16()
            elif t == "Uint32":
                value.val = reader.getUInt32()
            elif t == "CsUint8Enum":
                value.val = reader.getUInt8()
            elif t == "CsUint16Enum":
                value.val = reader.getUInt16()
            elif t == "Uint8Array":
                if value.size is None:
                    raise Exception("CANT_AUTOMATICALLY_PARSE_UINT8_ARRAY")
                value.val = reader.getBytes(value.size)
            elif t == "Uint16Array":
                if value.size is None:
                    raise Exception("CANT_AUTOMATICALLY_PARSE_UINT16_ARRAY")
                data = reader.getBytes(value.size)
                reader = BufferReader(data)

                while reader.getRemainingByteCount() > 1:
                    data.append(reader.getUInt16())
                value.val = data


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
        if val is None:
            val = 0
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint8_to_uint8_array(self.val)

    def setPacket(self, bytelist):
        if len(bytelist) < 1:
            raise ValueError("Deserialization failed, not enough bytes left")
        self.val = Conversion.uint8_array_to_uint8(bytelist[:1])
        return bytelist[1:]

    def __repr__(self):
        return f"{str(self.val)}"


class Uint16(IntPacket):
    def __init__(self, val=0):
        if val is None:
            val = 0
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint16_to_uint8_array(self.val)

    def setPacket(self, bytelist):
        if len(bytelist) < 2:
            raise ValueError("Deserialization failed, not enough bytes left")
        self.val = Conversion.uint8_array_to_uint16(bytelist[:2])
        return bytelist[2:]

    def __repr__(self):
        return f"{str(self.val)}"

class Uint32(PacketBase):
    def __init__(self, val=0):
        if val is None:
            val = 0
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint32_to_uint8_array(self.val)

    def __str__(self):
        return f"{str(self.val)}"


class Uint8Array(PacketBase):
    """
    Soon to be deprecated in favour of PacketBaseList(Uint8)
    """
    def __init__(self, val=[]):
        self.val = list([int(x) for x in val])

    def getPacket(self):
        return self.val

    def __repr__(self):
        return f"{str(self.val)}"



class Uint16Array(PacketBase):
    """
    Soon to be deprecated in favour of PacketBaseList(Uint16)
    """
    def __init__(self, val=[]):
        self.val = list([int(x) for x in val])

    def getPacket(self):
        return Conversion.uint16_array_to_uint8_array(self.val)

    def __repr__(self):
        return f"{str(self.val)}"

class PacketBaseList(PacketBase):
    """
    Wraps a generic list of descendants of PacketBase and packs them individually.
    Providing a cls parameter gives a type hint.

    Todo: access to array elements should preserve type safety.
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
        self.cls = cls

    def getPacket(self):
        packet = []
        for name, val in self.val:
            packet += val.getPacket()
        return packet

    def setPacket(self, bytelist):
        """
        PacketBaseList eats all remaining bytes of the list and assumes it
        can be used to fill an array of the type self.cls.
        """
        self.val = []
        while len(bytelist) > 0:
            newItem = self.cls()
            bytelist = newItem.setPacket(bytelist)
            self.val.append(newItem)
        return []


class CsUint8Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint8_to_uint8_array(int(self))


class CsUint16Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(int(self))
