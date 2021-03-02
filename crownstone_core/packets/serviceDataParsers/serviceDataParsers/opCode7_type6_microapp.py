import time
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.Timestamp import reconstructTimestamp
from crownstone_core.packets.serviceDataParsers.containers.AdvMicroappData import AdvMicroappData

def parseMicroappServiceData(reader: BufferReader):
    packet = AdvMicroappData()

    flags = reader.getUInt8()
    packet.microappUuid     = reader.getUInt16()
    packet.microappData     = reader.getBytes(8)
    packet.crownstoneId     = reader.getUInt8()
    packet.partialTimestamp = reader.getUInt16()
    packet.validation       = reader.getUInt8()

    packet.timeIsSet = flags & (1 << 0)
    packet.uniqueIdentifier = packet.partialTimestamp
    if packet.timeIsSet:
        packet.timestamp = reconstructTimestamp(time.time(), packet.partialTimestamp)
    else:
        packet.timestamp = packet.partialTimestamp # this is now a counter

    return packet
