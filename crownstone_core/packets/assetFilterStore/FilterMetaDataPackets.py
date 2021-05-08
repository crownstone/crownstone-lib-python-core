from crownstone_core.util.BasePackets import PacketBase, Uint8, Uint16, CsUint8Enum, Uint32, Uint8Array
from crownstone_core.packets.assetFilterStore.FilterDescriptionPackets import FilterInputType


class FilterMetaData(PacketBase):
    """
    ASSET_FILTER_STORE.md#tracking-filter-meta-data
    """
    def __init__(self, type: int, profileId: int, input: FilterFormatMacAddress or FilterFormatMaskedAdData or FilterFormatMaskedAdData, outputDescription: FilterOutputDescription):
        self.type              = Uint8(type)
        self.profileId         = Uint8(profileId)
        self.input             = Uint8Array(input.getPacket())
        self.outputDescription = Uint8Array(outputDescription.getPacket())

class TrackingFilterData(PacketBase):
    """
    ASSET_FILTER_STORE.md#tracking-filter-data
    This packet is part of the tracking filter command protocol, where it is chunked to fit in <= MTU sized messages
    """
    def __init__(self):
        self.metadata = TrackingFilterMetaData()
        self.filter = Uint8Array() # CuckooFilterData()


