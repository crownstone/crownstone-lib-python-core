from crownstone_core.packets.CrownstonePacket import *
from crownstone_core.protocol.BluenetTypes import ControlType

from enum import IntEnum


class SomeEnum(IntEnum):
    A = 0
    B = 1
    C = 2
    UNKNOWN = 255


# ----- core data types -------

class SunTimes(metaclass=CrownstonePacket):
    sunrise=Uint32()
    sunset=Uint32()
    some=Uint8Enum(cls=SomeEnum,default=SomeEnum.UNKNOWN)

    def __init__(self, *args, **kwargs):
        pass
        # self.sunrise = 13
        # self.sunset = 13

# ----- wrapper types -------


class ControlPacket(metaclass=CrownstonePacket):
    payloadTypeDict = {
        ControlType.SWITCH : Uint8(default=100),
        ControlType.SET_SUN_TIME : SunTimes(),
        ControlType.LOCK_SWITCH : Bool(default=True)
    }

    # PacketFormat
    protocol=Uint8()
    commandtype=Uint16Enum(cls=ControlType, default=ControlType.SWITCH)
    size=Uint16()
    payload=Variant(typeDict=payloadTypeDict, typeGetter=lambda x: x.commandtype)




# ----- usage -------

if __name__ == "__main__":
    s = SunTimes()
    s.sunrise = 9 * 60 * 60
    s.sunset = 21 * 60 * 60
    print("--------------")
    print("suntimes packet: ", s.serialize())
    print("--------------")
    packet = ControlPacket(commandtype=ControlType.SWITCH)
    # packet.payload = 99
    packet.payload
    print("ControlPacket, commandtype=switch:", packet.serialize())
    print("--------------")
    defaultpacket = ControlPacket()
    print("default packet", defaultpacket.serialize())
