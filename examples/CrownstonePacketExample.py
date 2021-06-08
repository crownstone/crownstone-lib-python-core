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
    getPayloadTypeDict = {
        ControlType.SWITCH : Uint8,
        ControlType.SET_SUN_TIME : SunTimes,
        ControlType.LOCK_SWITCH : Bool
    }

    # PacketFormat
    protocol=Uint8()
    packet=Uint16()
    size=Uint16()
    payload=Variant(typeDict=getPayloadTypeDict, typeGetter=lambda x: x.command)




# ----- usage -------

if __name__ == "__main__":
    s = SunTimes()
    s.sunrise = 9 * 60 * 60
    s.sunset = 21 * 60 * 60
    print("--------------")
    print("suntimes packet: ", s.getPacket())


if False and __name__ == "__main__":
    # construct with named arguments (or unnamed if you know all fields immediately)
    packet = ControlPacket(command=ControlType.LOCK_SWITCH)
    packet.payload = True
    print(packet.getPacket())

    # accessing a variant will check the typeGetter and load the correct
    # subobject so that the sunrise/sunset attributes are available
    packet.command = ControlType.SET_SUN_TIME
    packet.payload.sunrise = 9 * 60 * 60
    packet.payload.sunset = 21 * 60 * 60
    print(packet.getPacket())

    # load back the LOCK_SWITCH payload (or load default values)
    packet.command = ControlType.LOCK_SWITCH
    print(packet.getPacket())