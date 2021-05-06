import math

from crownstone_core.util.CRC import crc16ccitt

from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.packets.assetFilters.FilterMetaDataPackets import FilterMetaData
from crownstone_core.packets.assetFilters.FilterPackets import FilterUploadChunk


def getMasterCRC(inputData : [[int, int]]) -> int:
    """
        the input data is an array of [filterId, filterCRC] numbers
        This method is used to get the masterCRC
    """
    def sortMethod(val):
        return val[0]

    inputData.sort(key=sortMethod)
    writer = BufferWriter()

    for filterData in inputData:
        writer.putUInt16(filterData[1])

    return crc16ccitt(writer.getBuffer())

def getFilterCRC(metaData: FilterMetaData, filterData: [int]) -> int:
    """
        the input data is an array of [filterId, filterCRC] numbers
        This method is used to get the masterCRC
    """
    writer = BufferWriter()

    writer.putUInt8(metaData.type)
    writer.putBytes(metaData.input.getPacket())
    writer.putBytes(metaData.outputDescription.getPacket())
    writer.putUInt8(metaData.profileId)
    writer.putBytes(filterData)
    return crc16ccitt(writer.getBuffer())

class FilterChunker:

    def __init__(self, filterId: int, filterPacket: [int]):
        self.filterId = filterId
        self.filterPacket = filterPacket

        self.index = 0
        self.maxChunkSize = 256

    def getAmountOfChunks(self) -> int:
        totalSize = self.filterPacket.length
        count = math.floor(totalSize/self.maxChunkSize)
        if totalSize % self.maxChunkSize > 0:
            count += 1
        return count

    def getChunk(self) -> [int]:
        totalSize = self.filterPacket.length
        if totalSize > self.maxChunkSize:
            chunkSize = min(self.maxChunkSize, totalSize - self.maxChunkSize)
            chunkData = self.filterPacket[self.index*self.maxChunkSize:(self.index+1)*self.maxChunkSize]
            chunk = FilterUploadChunk(self.filterId, self.index, totalSize, chunkSize, chunkData).getPacket()
            self.index += 1
            return chunk
        else:
            return FilterUploadChunk(self.filterId, self.index, totalSize, totalSize, self.filterPacket).getPacket()


