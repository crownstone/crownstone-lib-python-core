from crownstone_core.util.BasePackets import *

from crownstone_core.packets.assetFilterStore.FilterIOPackets import *
from crownstone_core.packets.cuckoofilter.CuckooFilterPackets import *

class FilterMetaData(PacketBase):
    """
    ASSET_FILTER_STORE.md#tracking-filter-meta-data
    """
    def __init__(self, type: int, profileId: int, input: FilterFormatMacAddress or FilterFormatMaskedAdData or FilterFormatMaskedAdData, outputDescription: FilterOutputDescription):
        self.type              = Uint8(type)
        self.profileId         = Uint8(profileId)
        self.input             = FilterOutputDescription()
        self.outputDescription = Uint8Array(outputDescription.getPacket())

class AssetFilter(PacketBase):
    """
    ASSET_FILTER_STORE.md#tracking-filter-data
    This packet is part of the tracking filter command protocol, where it is chunked to fit in <= MTU sized messages
    """
    typeMap = {FilterType.CUCKOO : CuckooFilterData}

    def __init__(self):
        self.metadata = FilterMetaData()
        self.filter = PacketVariant(type_enum_to_type_dict=AssetFilter.typeMap,
                                    type_getter_lambda=lambda:self.metadata.type)


