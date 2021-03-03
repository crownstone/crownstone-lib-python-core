from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.util.BufferReader import BufferReader

from crownstone_core.packets.serviceDataParsers.parsers import parseOpCode6, parseOpcode7
from crownstone_core.protocol.BluenetTypes import DeviceType
from crownstone_core.util.EncryptionHandler import EncryptionHandler


class ServiceData:
    
    def __init__(self, data, unencrypted = False):
        self.opCode = 0
        self.dataType = 0
        self.deviceType = DeviceType.UNDEFINED
        self.payload = None

        self.data = data
        self.parse(unencrypted)

    def _parse(self, data):
        reader      = BufferReader(data)
        self.opCode = reader.getUInt8()
        deviceType  = reader.getUInt8()
        if DeviceType.has_value(deviceType):
            self.deviceType = DeviceType(deviceType)

        if self.opCode == 7:
            self.payload = parseOpcode7(self, reader.getRemainingBytes())
        elif self.opCode == 6:
            self.payload = parseOpCode6(self, reader.getRemainingBytes())
        else:
            raise CrownstoneException(CrownstoneError.INVALID_SERVICE_DATA, "Protocol not supported.")


    def decrypt(self, keyHexString):
        if self.validData and len(self.encryptedData) == 16 and len(keyHexString) >= 16:
            if not self.setupMode:
                result = EncryptionHandler.decryptECB(self.encryptedData, keyHexString)

                for i in range(0, len(self.encryptedData)):
                    self.data[i + self.encryptedDataStartIndex] = result[i]

                self.parse()
            self.dataReadyForUse = True
        else:
            self.dataReadyForUse = False

