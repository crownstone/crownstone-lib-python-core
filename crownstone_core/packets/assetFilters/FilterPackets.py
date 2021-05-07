import math

from crownstone_core.util.BasePackets import *

# This will be changed once we actually support 2 different protocol versions.
ASSET_FILTER_PROTOCOL = 0

class AssetFilterCommand(PacketBase):

    def __init__(self):
        self.assetFilterProtocol = Uint8(ASSET_FILTER_PROTOCOL)
        self.payload = Uint8Array()


class FilterUploadChunk(PacketBase):

    def __init__(self, filterId: int = 0, chunkStartIndex: int = 0, totalSize: int = 0, chunkSize: int = 0, chunk : [int] = None):
        self.filterId = Uint8(filterId)
        self.chunkStartIndex = Uint16(chunkStartIndex)
        self.totalSize = Uint16(totalSize)
        self.chunkSize = Uint16(chunkSize)
        self.chunk = Uint8Array(chunk)


FILTER_SUMMARY_SIZE = 4
class FilterSummaries:

    def __init__(self):
        self.supportedFilterProtocol : int = 0
        self.masterVersion : int = 0
        self.masterCrc     : int = 0
        self.freeSpaceLeft : int = 0
        self.summaries     : [FilterSummary] = []

    def fromData(self, data: [int]):
        reader = BufferReader(data)
        self.supportedFilterProtocol = reader.getUInt8()
        self.masterVersion           = reader.getUInt16()
        self.masterCrc               = reader.getUInt16()
        self.freeSpaceLeft           = reader.getUInt16()

        amountOfFilters = int(math.floor(reader.getRemainingByteCount() / FILTER_SUMMARY_SIZE))

        for i in range(0, amountOfFilters):
            summary = FilterSummary()
            summary.fromData(reader.getBytes(FILTER_SUMMARY_SIZE))
            self.summaries.append(summary)

class FilterSummary(PacketBase):

    def __init__(self):
        self.filterId   = Uint8()
        self.filterType = Uint8()
        self.filterCrc  = Uint16()
