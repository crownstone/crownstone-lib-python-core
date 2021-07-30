from crownstone_core.packets.assetFilter.FilterMetaDataPackets import FilterMetaData

from crownstone_core.packets.assetFilter.CuckooFilterPackets import CuckooFilterData
from crownstone_core.packets.assetFilter.ExactMatchFilter import ExactMatchFilter
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *
from crownstone_core.util.BufferWriter import BufferWriter

class AssetFilter(BasePacket):
    """
    This is the packet that is uploaded.
    """
    def __init__(self,
                 metaData: FilterMetaData = None,
                 filterData: CuckooFilterData or ExactMatchFilter = None):
        self.metaData = metaData
        self.filterData = filterData

    def _toBuffer(self, writer: BufferWriter):
        self.metaData.toBuffer(writer)
        self.filterData.toBuffer(writer)

    def __str__(self):
        return f"AssetFilter(" \
               f"metaData={self.metaData} " \
               f"filterData={self.filterData})"


class AssetFilterAndId:
    def __init__(self, filterId: int, filter: AssetFilter):
        self.id = filterId
        self.filter = filter
