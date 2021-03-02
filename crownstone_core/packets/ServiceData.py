from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.util.BufferReader import BufferReader

from crownstone_core.packets.CrownstoneErrors import CrownstoneErrors
from crownstone_core.packets.serviceDataParsers.parsers import parseOpCode5, parseOpCode6, parseOpCode4, parseOpCode3, parseOpcode7
from crownstone_core.protocol.BluenetTypes import DeviceType
from crownstone_core.protocol.SwitchState import SwitchState
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

    # def parse(self, unencrypted=False):
    #     reader = BufferReader(self.data)
    #     self.opCode = reader.getUInt8()
    #
    #     if len(self.data) == 18:
    #         self.opCode = self.data[0]
    #         self.encryptedData = self.data[2:]
    #         self.encryptedDataStartIndex = 2
    #     else:
    #         self.validData = False
    #
    #     if self.validData:
    #         if self.opCode == 7:
    #             self.getDeviceTypeFromPublicData()
    #             self.payload = parseOpCode5(self, self.encryptedData)
    #         elif self.opCode == 6:
    #             self.getDeviceTypeFromPublicData()
    #             self.payload = parseOpCode6(self, self.encryptedData)
    #         else:
    #             self.getDeviceTypeFromPublicData()
    #             parseOpCode5(self, self.encryptedData)

    def isInSetupMode(self):
        if not self.validData:
            return False
    
        return self.setupMode
    
    
    # def getDictionary(self):
    #     errorsDictionary = CrownstoneErrors(self.errorsBitmask).getDictionary()
    #
    #     returnDict = {}
    #
    #     returnDict["opCode"]                    = self.opCode
    #     returnDict["dataType"]                  = self.dataType
    #     returnDict["stateOfExternalCrownstone"] = self.stateOfExternalCrownstone
    #     returnDict["hasError"]                  = self.hasError
    #     returnDict["setupMode"]                 = self.isInSetupMode()
    #     returnDict["id"]                        = self.crownstoneId
    #     returnDict["switchState"]               = self.switchState.raw
    #     returnDict["flagsBitmask"]              = self.flagsBitmask
    #     returnDict["temperature"]               = self.temperature
    #     returnDict["powerFactor"]               = self.powerFactor
    #     returnDict["powerUsageReal"]            = self.powerUsageReal
    #     returnDict["powerUsageApparent"]        = self.powerUsageApparent
    #     returnDict["accumulatedEnergy"]         = self.accumulatedEnergy
    #     returnDict["timestamp"]                 = self.timestamp
    #     returnDict["dimmerReady"]               = self.dimmerReady
    #     returnDict["dimmingAllowed"]            = self.dimmingAllowed
    #     returnDict["switchLocked"]              = self.switchLocked
    #     returnDict["switchCraftEnabled"]        = self.switchCraftEnabled
    #     returnDict["tapToToggleEnabled"]        = self.tapToToggleEnabled
    #     returnDict["behaviourEnabled"]          = self.behaviourEnabled
    #     returnDict["behaviourOverridden"]       = self.behaviourOverridden
    #     returnDict["behaviourMasterHash"]       = self.behaviourMasterHash
    #
    #     returnDict["errorMode"]                 = self.errorMode
    #     returnDict["errors"]                    = errorsDictionary
    #
    #     returnDict["uniqueElement"]             =  self.uniqueIdentifier
    #     returnDict["timeIsSet"]                 =  self.timeIsSet
    #
    #     returnDict["rssiOfExternalCrownstone"]  = self.rssiOfExternalCrownstone
    #
    #     returnDict["microappUuid"]              = self.microappUuid
    #     returnDict["microappData"]              = list(self.microappData)
    #
    #     return returnDict
    #
    #
    # def getSummary(self, address):
    #     errorsDictionary = CrownstoneErrors(self.errorsBitmask).getDictionary()
    #
    #     returnDict = {}
    #
    #     returnDict["id"] = self.crownstoneId
    #     returnDict["address"] = address
    #     returnDict["setupMode"] = self.isInSetupMode()
    #     returnDict["switchState"] = self.switchState.raw
    #     returnDict["temperature"] = self.temperature
    #     returnDict["powerFactor"] = self.powerFactor
    #     returnDict["powerUsageReal"] = self.powerUsageReal
    #     returnDict["powerUsageApparent"] = self.powerUsageApparent
    #     returnDict["accumulatedEnergy"] = self.accumulatedEnergy
    #     returnDict["dimmerReady"] = self.dimmerReady
    #     returnDict["dimmingAllowed"] = self.dimmingAllowed
    #     returnDict["switchLocked"] = self.switchLocked
    #     returnDict["switchCraftEnabled"] = self.switchCraftEnabled
    #     returnDict["timeIsSet"] = self.timeIsSet
    #     returnDict["timestamp"] = self.timestamp
    #     returnDict["hasError"] = self.hasError
    #     returnDict["errorMode"] = self.errorMode
    #     returnDict["errors"] = errorsDictionary
    #
    #     return returnDict


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

