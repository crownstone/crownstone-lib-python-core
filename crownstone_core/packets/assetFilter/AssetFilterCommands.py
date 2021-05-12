from crownstone_core.util.BasePackets import *
from crownstone_core.packets.assetFilter.FilterDescriptionPackets import FilterSummary


ASSET_FILTER_PROTOCOL = Uint8(0)

class UploadFilterCommandPacket(PacketBase):
    """
    Packet definition for upload filter control command.
    """
    def __init__(self, filterId, chunkStartIndex, totalSize, chunkSize, chunk: [int]):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.filterId = Uint8(filterId)
        self.chunkStartIndex = Uint16(chunkStartIndex)
        self.totalSize = Uint16(totalSize)
        self.chunkSize = Uint16(chunkSize)
        self.chunk = Uint8Array(chunk)

class RemoveFilterCommandPacket(PacketBase):
    """
     Packet definition for remove filter control command.
    """
    def __init__(self, filterId=None):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.filterId = Uint8(filterId if filterId is not None else 0)

class CommitFilterChangesCommandPacket(PacketBase):
    """
     Packet definition for commit filter changes control command.
    """
    def __init__(self):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.masterVersion = Uint16()
        self.masterCrc = Uint16()

class GetFilterSummariesReturnPacket(PacketBase):
    """
    Definition of result packet for get filter summaries control command.
    """
    def __init__(self):
        self.commandProtocolVersion = Uint8()
        self.masterVersion = Uint16()
        self.masterCrc = Uint16()
        self.freeSpace = Uint16()
        self.summaries = PacketBaseList(cls=FilterSummary)
