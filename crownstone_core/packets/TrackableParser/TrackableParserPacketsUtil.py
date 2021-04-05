from enum import IntEnum
from crownstone_core.util.Conversion import Conversion

# -------------------------------
# ------ lib/util stuff ---------
# -------------------------------

class PacketBase:
    def getPacket(self):
        """
        Serializes the whole object
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
            tv = type(value)
            if t is not tv:
                value = t(value)
        self.__dict__[name] = value


# ----- literal types -------

class Uint8:
    def __init__(self, val = 0):
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint8_to_uint8_array(self.val)


class Uint16:
    def __init__(self, val = 0):
        self.val = int(val)

    def getPacket(self):
        return Conversion.uint16_to_uint8_array(self.val)


class Uint8Array:
    def __init__(self, val = None):
        if val is None:
            self.val = []
        else:
            self.val = list(val)

    def getPacket(self):
        return self.val

class Uint16Array:
    def __init__(self, val = None):
        if val is None:
            self.val = []
        else:
            self.val = list(val)

    def getPacket(self):
        return Conversion.uint16_array_to_uint8_array(self.val)

class CsEnum8(IntEnum):
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(int(self))

class CsEnum16(IntEnum):
    def getPacket(self):
        return Conversion.uint16_to_uint8_array(int(self))
