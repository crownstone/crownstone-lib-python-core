from crownstone_core.packets.assetFilter.FilterIOPackets import *
from crownstone_core.packets.assetFilter.FilterDescriptionPackets import *
from crownstone_core.packets.cuckoofilter.CuckooFilterPackets import *
from crownstone_core.packets.exactMatchFilter.ExactMatchFilter import ExactMatchFilterData

from crownstone_core.util.BasePackets import *

"""
TODO: rename packets
TODO: add constructors
"""

class FilterMetaData(PacketBase):
    """
    Common metadata of an asset filter.
    """
    def __init__(self):
        self.type              = FilterType.CUCKOO
        self.flags             = Uint8()
        self.profileId         = Uint8()
        self.inputDescription  = FilterInputDescription()
        self.outputDescription = FilterOutputDescription()

class AssetFilter(PacketBase):
    """
    This is the packet that is uploaded.
    """
    typeMap = {
        FilterType.CUCKOO : CuckooFilterData,
        FilterType.EXACT_MATCH : ExactMatchFilterData,
    }

    def __init__(self):
        self.metadata = FilterMetaData()
        self.filterdata = PacketVariant(type_enum_to_type_dict=AssetFilter.typeMap,
                                    type_getter_lambda=lambda:self.metadata.type)

class AssetFilterAndId:
    filter: AssetFilter
    id: int

    def __init__(self, filterId: int, filter: AssetFilter):
        self.id = filterId
        self.filter = filter
