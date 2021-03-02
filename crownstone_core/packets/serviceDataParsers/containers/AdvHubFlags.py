from crownstone_core.util.Conversion import Conversion


class AdvHubFlags:

    def __init__(self, byte):
        bitmaskArray = Conversion.uint8_to_bit_array(byte)

        self.uartAlive                          = bitmaskArray[0]
        self.uartAliveEncrypted                 = bitmaskArray[1]
        self.uartEncryptionRequiredByCrownstone = bitmaskArray[2]
        self.uartEncryptionRequiredByHub        = bitmaskArray[3]
        self.hubHasBeenSetUp                    = bitmaskArray[4]
        self.hubHasInternet                     = bitmaskArray[5]
        self.hubHasError                        = bitmaskArray[6]
        self.timeIsSet                          = bitmaskArray[7]
