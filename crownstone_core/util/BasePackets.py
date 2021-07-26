"""
An interface base to define packet formats in short and concise fashion.

Example usage can (for now) be found in ExampleBasePackets.py
"""

from enum import IntEnum

from crownstone_core.util.BufferReader import BufferReader

from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.Bitmasks import Bitmasks

# TODO: there's already a BasePacket class, will this class replace it?
# TODO: does CrownstonePacket replace this class?
class PacketBase:
    def getPacket(self):
        """
        Serializes the whole object by calling getPacket on each member variable and
        appending the return values to a list of uint8s.

        Fields are None-checked to allow for easy optional fields at runtime.
        """
        # TODO: add BufferWriter as arugment with default value None.
        # if the writer is not None it will be easier to optimize for
        # repeated writes instead of the += operator, which will likely
        # incur more copying.
        packet = []
        for name, val in self.__dict__.items():
            if val is not None:
                packet += val.getPacket()
        return packet

    def setPacket(self, bytelist):
        """
        Loads the object from the given bytelist, returning the tail of the bytelist
        consisting of all bytes that weren't used by this setPacket call.

        Failure to setPacket invocations are required to throw an exception of type ValueError.
        Fields that have the type None type are ignored.
        """
        # TODO: add BufferReader as arugment with default value None.
        # if the writer is not None it will be easier to optimize for
        # repeated writes instead of the += operator, which will likely
        # incur more copying.
        for name, val in self.__dict__.items():
            if type(val) is not type(None):
                bytelist = val.setPacket(bytelist)
        return bytelist


    def __setattr__(self, name, value):
        """
        Enforces type equality after assignment.
        Allows fields of type None to be set to a different type
        """
        if name in self.__dict__:
            t = type(self.__dict__[name])
            if t is not type(value) and t is not type(None):
                # try to cast 'value' to the type that self.name already has, unless self.name is None.
                value = t(value)
        self.__dict__[name] = value

    def __repr__(self):
        return "{0}({1})".format(
            type(self).__name__,
            ", ".join([f"{k}: {str(v)}" for k, v in self.__dict__.items()])
        )

    def __eq__(self, other):
        return self.getPacket() == other.getPacket()

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
    def __init__(self, val=None):
        if val is None:
            self.val = 0
        else:
            self.val = int(val)

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

    def __str__(self):
        return f"{str(self.val)}"


# ----- literal types -------

class Uint8(IntPacket):
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
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(self.val)

    def setPacket(self, bytelist):
        if len(bytelist) < 2:
            raise ValueError("Deserialization failed, not enough bytes left")
        self.val = Conversion.uint8_array_to_uint16(bytelist[:2])
        return bytelist[2:]


class Uint32(IntPacket):
    def getPacket(self):
        return Conversion.uint32_to_uint8_array(self.val)

    def setPacket(self, bytelist):
        if len(bytelist) < 4:
            raise ValueError("Deserialization failed, not enough bytes left")
        self.val = Conversion.uint8_array_to_uint32(bytelist[:4])
        return bytelist[4:]



class Int8(IntPacket):
    def getPacket(self):
        return Conversion.uint8_to_int8_array(self.val)

    def setPacket(self, bytelist):
        if len(bytelist) < 1:
            raise ValueError("Deserialization failed, not enough bytes left")
        self.val = Conversion.uint8_array_to_int8(bytelist[:1])
        return bytelist[1:]

    def __repr__(self):
        return f"{str(self.val)}"


class CsUint8Enum(IntEnum):
    def getPacket(self):
        return Conversion.uint8_to_uint8_array(int(self))

    def setPacket(self, bytelist):
        raise NotImplementedError("Can't deserialize enums yet. Python enums are peculiar, this still needs an implementation")
        return bytelist[1:]


class CsUint16Enum(IntPacket):
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(self.val)

    def setPacket(self, bytelist):
        raise NotImplementedError("Can't deserialize enums yet. Python enums are peculiar, this still needs an implementation")
        return bytelist[2:]

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
    cls: the type of elements in the array.
    len: (optional) the number of elements in the array.

    Todo: access to array elements should preserve type safety.
    """
    def __init__(self, cls=None, val=[], len=None):
        if cls is None:
            raise ValueError("cls is required")
        if type(cls) is not type:
            raise ValueError("cls must be a type object")
        if not issubclass(cls, PacketBase):
            raise ValueError("cls must be a type object subclassing PacketBase")

        # try to cast value to the correct type if that wasn't the case yet.
        self.val = [value if type(value) is cls else cls(value) for value in val]
        self.cls = cls
        self.len = int(len) if len is not None else None

    def getPacket(self):
        packet = []
        for v in self.val:
            if type (v) != self.cls:
                v = self.cls(v)
            packet += v.getPacket()
        return packet

    def setPacket(self, bytelist):
        """
        PacketBaseList eats all remaining bytes of the list and assumes it
        can be used to fill an array of the type self.cls.
        """
        self.val = []
        if self.len is None:
            while len(bytelist) > 0:
                newItem = self.cls()
                bytelist = newItem.setPacket(bytelist)
                self.val.append(newItem)
        else:
            for i in range(self.len):
                newItem = self.cls()
                bytelist = newItem.setPacket(bytelist)
                self.val.append(newItem)
        return bytelist
    #
    # def __eq__(self, other):
    #     print("PacketBaseList __eq__")
    #     return self.getPacket() == other.getPacket()


class PacketVariant(PacketBase):
    """
    Defines a field whose type depends on the surrounding packet
    """
    def __init__(self, type_enum_to_type_dict, type_getter_lambda):
        self.typedict = type_enum_to_type_dict
        self.typegetter = type_getter_lambda
        self.val = None

    def currentType(self):
        return self.typedict[self.typegetter()]

    def loadType(self):
        """
        Default constructs self.val based on the current value of the surrounding object.
        Can only be called once, afterwards the type of val is fixed by PacketBase.__setattr__.
        """
        self.val = self.currentType()()

    def getPacket(self):
        """
        Will call self.loadType() if val is none.
        """
        if self.val is None:
            # might not be loaded yet
            self.loadType()
        if type(self.val) is not self.currentType():
            raise ValueError("Type mismatch while serializing PacketVariant. Should be {0} according to typegetter, but object was of type: {1}".format(self.currentType(), type(self.val)))
        if self.val is None:
            return []
        return self.val.getPacket()

    def setPacket(self, bytelist):
        if self.val is None:
            # this is the tea: while deserializing the current type will already have been set
            # so by the time this setPacket call is made we can load a default constructed object
            # of correct type and continue as if nothing complicated is going on.
            self.loadType()
        return self.val.setPacket()
