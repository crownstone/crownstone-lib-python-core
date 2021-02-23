import time

from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.DataStepper import DataStepper
from crownstone_core.util.Timestamp import reconstructTimestamp

# Microapp data
def parseOpCode7_type6(serviceData, data):
    if len(data) == 16:
        # dataType = data[0]
        
        serviceData.stateOfExternalCrownstone = False

        payload = DataStepper(data)

        payload.skip() # first byte is the datatype.

        flags = payload.getUInt8()
        serviceData.microappUuid = payload.getUInt16()
        serviceData.microappData = payload.getAmountOfBytes(8)
        serviceData.crownstoneId = payload.getUInt8()
        serviceData.partialTimestamp = payload.getUInt16()
        serviceData.validation = payload.getUInt8()

        serviceData.timeIsSet = flags & (1 << 0)
        serviceData.uniqueIdentifier = serviceData.partialTimestamp
        if serviceData.timeIsSet:
            serviceData.timestamp = reconstructTimestamp(time.time(), serviceData.partialTimestamp)
        else:
            serviceData.timestamp = serviceData.partialTimestamp # this is now a counter
