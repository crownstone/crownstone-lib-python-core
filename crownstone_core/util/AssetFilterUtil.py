from crownstone_core.packets.assetFilter.AssetFilterCommands import UploadFilterCommandPacket
from crownstone_core.packets.assetFilter.FilterMetaDataPackets import AssetFilter, AssetFilterAndId
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.CRC import crc32
import math

def get_master_crc_from_filters(filters: [AssetFilterAndId]) -> int:
    input_data = []
    for filter in filters:
        id = filter.id
        crc = get_filter_crc(filter.filter)
        input_data.append([id, crc])
    return get_master_crc_from_filter_crcs(input_data)

def get_master_crc_from_filter_crcs(input_data : [[int, int]]) -> int:
    """
        the input data is an array of [filterId, filterCRC] numbers
        This method is used to get the masterCRC
    """
    def sort_method(val):
        return val[0]

    input_data.sort(key=sort_method)
    writer = BufferWriter()

    for id_and_filter_crc in input_data:
        writer.putUInt8(id_and_filter_crc[0])
        writer.putUInt32(id_and_filter_crc[1]) # TODO: use packets to serialize.

    return crc32(writer.getBuffer())

def get_filter_crc(filter: AssetFilter) -> int:
    """
    """
    return crc32(filter.getPacket())

class FilterChunker:

    def __init__(self, filterId: int, filterPacket: [int]):
        self.filterId = filterId
        self.filterPacket = filterPacket

        self.index = 0
        self.maxChunkSize = 256

    def getAmountOfChunks(self) -> int:
        totalSize = len(self.filterPacket)
        count = math.floor(totalSize/self.maxChunkSize)
        if totalSize % self.maxChunkSize > 0:
            count += 1
        return count

    def getChunk(self) -> [int]:
        totalSize = len(self.filterPacket)
        if totalSize > self.maxChunkSize:
            chunkSize = min(self.maxChunkSize, totalSize - self.maxChunkSize)
            chunkData = self.filterPacket[self.index * self.maxChunkSize : (self.index + 1) * self.maxChunkSize]
            cmd = UploadFilterCommandPacket(self.filterId, self.index, totalSize, chunkSize, chunkData)
            self.index += 1
            return cmd.getPacket()
        else:
            return UploadFilterCommandPacket(self.filterId, self.index, totalSize, totalSize, self.filterPacket).getPacket()


