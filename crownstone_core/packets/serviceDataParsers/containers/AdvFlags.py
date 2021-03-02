from crownstone_core.util.Conversion import Conversion


class AdvFlags:

    def __init__(self, byte):
        bitmaskArray = Conversion.uint8_to_bit_array(byte)

        self.dimmerReady         = bitmaskArray[0]
        self.dimmingAllowed      = bitmaskArray[1]
        self.hasError            = bitmaskArray[2]
        self.switchLocked        = bitmaskArray[3]
        self.timeIsSet           = bitmaskArray[4]
        self.switchCraftEnabled  = bitmaskArray[5]
        self.tapToToggleEnabled  = bitmaskArray[6]
        self.behaviourOverridden = bitmaskArray[7]
