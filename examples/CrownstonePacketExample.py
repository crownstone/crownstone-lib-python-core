from crownstone_core.packets.CrownstonePacket import *
from crownstone_core.protocol.BluenetTypes import ControlType


# ----- core data types -------

class SunTimes(metaclass=CrownstonePacket):
    sunrise=Uint32()
    sunset=Uint32()

    def __init__(self, *args, **kwargs):
        print("--- SunTimes init --- ")
        self.sunrise = 0
        self.sunset = 0
        print (" ~~~")

# ----- wrapper types -------

def getControlPacketTypes():
    """ defines which ControlType is mapped to which formatted type """
    return {
        ControlType.SWITCH : Uint8,
        ControlType.SET_SUN_TIME : SunTimes,
        ControlType.LOCK_SWITCH : Bool
    }

class ControlPacket(metaclass=CrownstonePacket):
    protocol=Uint8()
    packet=Uint16()
    size=Uint16()
    payload=Variant(typeDict=getControlPacketTypes(), typeGetter=lambda x: x.command)



# ----- usage -------

if __name__ == "__main__":
    s = SunTimes()
    print("--------------")
    print(s.__dict__)
    print(s._packetFieldTypes)


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