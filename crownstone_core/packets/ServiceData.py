from crownstone_core.Enums import CrownstoneOperationMode

from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.packets.serviceDataParsers.parsers import parseOpCode6, parseOpcode7
from crownstone_core.protocol.BluenetTypes import DeviceType
from crownstone_core.util.EncryptionHandler import EncryptionHandler


class ServiceData:
    
    def __init__(self, data):
        self.opCode        = 0
        self.dataType      = 0
        self.deviceType    = DeviceType.UNDEFINED
        self.operationMode = CrownstoneOperationMode.UNKNOWN
        self.payload       = None
        self.encryptedData = None
        self.decrypted     = False

        self.data = data
        self.parse(data)

    def parse(self, data):
        reader      = BufferReader(data)
        self.opCode = reader.getUInt8()
        deviceType  = reader.getUInt8()
        if DeviceType.has_value(deviceType):
            self.deviceType = DeviceType(deviceType)

        if self.opCode == 7:
            self.encryptedData = reader.getRemainingBytes()
            self.payload = parseOpcode7(reader.getRemainingBytes())
            self.operationMode = CrownstoneOperationMode.NORMAL
        elif self.opCode == 6:
            self.payload = parseOpCode6(reader.getRemainingBytes())
            self.operationMode = CrownstoneOperationMode.SETUP
        else:
            raise CrownstoneException(CrownstoneError.INVALID_SERVICE_DATA, "Protocol not supported.")

    def getOperationMode(self):
        return self.operationMode

    def decrypt(self, keyHexString):
        if len(self.encryptedData) == 16 and len(keyHexString) >= 16 and len(self.data) == 18:
            if self.operationMode == CrownstoneOperationMode.NORMAL:
                result = EncryptionHandler.decryptECB(self.encryptedData, keyHexString)

                for i in range(0, len(self.encryptedData)):
                    # the first 2 bytes are opcode and device type
                    self.data[i + 2] = result[i]

                self.parse()
                self.decrypted = True
        else:
            raise CrownstoneException(CrownstoneError.COULD_NOT_DECRYPT)

