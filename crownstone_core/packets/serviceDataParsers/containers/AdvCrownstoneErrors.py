from crownstone_core.util.Conversion import Conversion
from crownstone_core.packets.serviceDataParsers.containers import AdvTypes


class AdvCrownstoneErrors:
    
    def __init__(self, bitMask):
        self.type = AdvTypes.CROWNSTONE_ERRORS

        self.bitMask = bitMask
    
        bitArray = Conversion.uint32_to_bit_array_reversed(bitMask)
    
        self.overCurrent        = bitArray[31 - 0]
        self.overCurrentDimmer  = bitArray[31 - 1]
        self.temperatureChip    = bitArray[31 - 2]
        self.temperatureDimmer  = bitArray[31 - 3]
        self.dimmerOnFailure    = bitArray[31 - 4]
        self.dimmerOffFailure   = bitArray[31 - 5]
