import math

from crownstone_core.packets.assetFilter.AssetFilterPackets import AssetFilter
from crownstone_core.packets.assetFilter.FilterCommandPackets import UploadFilterChunkPacket


class FilterChunker:

    def __init__(self, filterId: int, assetFilter: AssetFilter, maxChunkSize=128):
        self.filterId = filterId
        self.filterBuffer = assetFilter.toBuffer()

        self.index = 0
        self.maxChunkSize = maxChunkSize

    def getAmountOfChunks(self) -> int:
        totalSize = len(self.filterBuffer)
        count = math.floor(totalSize/self.maxChunkSize)
        if totalSize % self.maxChunkSize > 0:
            count += 1
        return count

    def getChunk(self) -> [int]:
        totalSize = len(self.filterBuffer)
        if totalSize > self.maxChunkSize:
            chunkSize = min(self.maxChunkSize, totalSize - self.index)
            chunkData = self.filterBuffer[self.index : self.index + chunkSize]
            cmd = UploadFilterChunkPacket(self.filterId, self.index, totalSize, chunkSize, chunkData)
            self.index += self.maxChunkSize
            return cmd.toBuffer()
        else:
            return UploadFilterChunkPacket(self.filterId, self.index, totalSize, totalSize, self.filterBuffer).toBuffer()
