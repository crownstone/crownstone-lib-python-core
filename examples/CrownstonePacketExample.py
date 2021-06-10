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
    sunrise  = Uint32(9*60*60)
    sunset   = Uint32(default=18*60*60)
    some     = Uint8Enum(cls=SomeEnum,default=SomeEnum.UNKNOWN)


class NestedSunTimes(metaclass=CrownstonePacket):
    suntimes = SunTimes()

# ----- wrapper types -------


class ControlPacket(metaclass=CrownstonePacket):
    payloadTypeDict = {
        ControlType.SWITCH : Uint8(default=100),
        ControlType.SET_SUN_TIME : SunTimes(),
        ControlType.LOCK_SWITCH : Bool(default=True)
    }

    # PacketFormat
    protocol    = Uint8()
    commandtype = Uint16Enum(cls=ControlType, default=ControlType.SWITCH)
    size        = Uint16()
    payload     = Variant(typeDict=payloadTypeDict, typeGetter=lambda x: x.commandtype)




# ----- usage -------

def sun():
    print("\n------- sun -------")
    s = SunTimes()
    s.sunrise = 9 * 60 * 60
    s.sunset = 21 * 60 * 60
    s.some = SomeEnum.C
    sSerialized = s.serialize()
    print("serialized: ", sSerialized)
    s1 = SunTimes()
    s1.deserialize(sSerialized)
    print("deserialized and then serialized: ", s1.serialize())

def controlswitch():
    print("\n------ controlswitch --------")
    packet = ControlPacket(commandtype=ControlType.SWITCH) # TODO: setting payload raised exception?
    serializedPacket = packet.serialize()
    print("serialized:", serializedPacket)

    packet1 = ControlPacket()
    packet1.deserialize(serializedPacket)
    print("deserialized and then serialized: ", packet1.serialize())

def controlsuntimes():
    print("\n------- controlsuntimes -------")
    packet = ControlPacket(commandtype=ControlType.SET_SUN_TIME)
    packet.payload.sunrise = 9 * 60 * 60
    packet.payload.sunset = 21 * 60 * 60
    packet.payload.some = SomeEnum.C

    serializedPacket = packet.serialize()
    print("serialized: ", serializedPacket)

    packet1 = ControlPacket()
    packet1.deserialize(serializedPacket)
    print("deserialized and then serialized", packet1.serialize())

def default():
    print("\n-------- default ------")
    defaultpacket = ControlPacket()
    print("default packet", defaultpacket.serialize())


def nested():
    print("\n------- nested -------")
    wrapped = NestedSunTimes()
    print("wrapped suntimes: ", wrapped.serialize())

def positional():
    print("\n------- positional -------")
    s = SunTimes(9*60*60, 18*60*60)
    print("constructed from positional arguments: ", s.serialize())

if __name__ == "__main__":
    sun()
    controlswitch()
    controlsuntimes()
    default()
    positional()
    nested()

