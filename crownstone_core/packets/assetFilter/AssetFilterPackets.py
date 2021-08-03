from crownstone_core.packets.assetFilter.FilterMetaDataPackets import FilterMetaData

from crownstone_core.packets.assetFilter.CuckooFilterPackets import CuckooFilterData
from crownstone_core.packets.assetFilter.ExactMatchFilter import ExactMatchFilter
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *
from crownstone_core.util.BufferWriter import BufferWriter

class AssetFilter(BasePacket):
    """
    A complete asset filter.
    It is recommended to use the AssetFilterBuilder to construct this class.
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
