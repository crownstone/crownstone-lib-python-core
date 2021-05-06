"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in ExampleBasePackets.py
"""

from enum import IntEnum

from crownstone_core.util.BufferReader import BufferReader

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
                value = t(value)
        self.__dict__[name] = value

    def __str__(self):
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


# ----- literal types -------
class Int8(PacketBase):
    def __init__(self, val=0):
        if val is None:
            val = 0
        self.val = int(val)

    def getPacket(self):
        return [Conversion.int8_to_uint8(self.val)]

    def __str__(self):
        return f"{str(self.val)}"

class Uint8(PacketBase):
    def __init__(self, val=0):
        if val is None:
            val = 0
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint8_to_uint8_array(self.val)

    def __str__(self):
        return f"{str(self.val)}"



class Uint16(PacketBase):
    def __init__(self, val=0):
        if val is None:
            val = 0
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint16_to_uint8_array(self.val)

    def __str__(self):
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
    def __init__(self, val=[], size : int = None):
        """
        The size here is used to allow fromData parsing. It is optional for normal usage.
        """
        self.size = size
        if val is None:
            val = []
        self.val = list([int(x) for x in val])

    def getPacket(self):
        return self.val

    def __str__(self):
        return f"{str(self.val)}"



class Uint16Array(PacketBase):
    def __init__(self, val=[], size : int = None):
        """
        The size here is used to allow fromData parsing. It is optional for normal usage.
        """
        self.size = size
        if val is None:
            val = []
        self.val = list([int(x) for x in val])

    def getPacket(self):
        return Conversion.uint16_array_to_uint8_array(self.val)

    def __str__(self):
        return f"{str(self.val)}"


class CsUint8Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint8_to_uint8_array(int(self))


class CsUint16Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(int(self))