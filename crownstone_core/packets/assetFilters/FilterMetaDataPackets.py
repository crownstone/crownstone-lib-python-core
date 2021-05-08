from crownstone_core.util.BasePackets import PacketBase, Uint8, Uint16, CsUint8Enum, Uint32, Uint8Array
from crownstone_core.packets.assetFilters.FilterTypes import FilterInputType


class FilterFormatMacAddress(PacketBase):
    """
    FilterInputType.MAC_ADDRESS
    """
    def __init__(self):
        pass


class FilterFormatAdData(PacketBase):
    """
    FilterInputType.AD_DATA
    """
    def __init__(self, adType: int):
        self.adType = Uint8(adType)


class FilterFormatMaskedAdData(PacketBase):
    """
    FilterInputType.MASKED_AD_DATA
    """
    def __init__(self, adType: int, mask: int):
        self.adType = Uint8(adType)
        self.mask   = Uint32(mask)


class FilterOutputDescription(PacketBase):
    """
    TRACKABLE_PARSER.md#advertisement-subdata-type
    """
    def __init__(self, output_type: int, formatPacket : FilterFormatMacAddress or FilterFormatMacAddress or FilterFormatMaskedAdData = None):
        self.type = Uint8(output_type)
        if formatPacket is not None:
            self.format = Uint8Array(formatPacket.getPacket())


class FilterMetaData(PacketBase):
    """
    TRACKABLE_PARSER.md#tracking-filter-meta-data
    """
    def __init__(self, type: int, profileId: int, input: FilterFormatMacAddress or FilterFormatMaskedAdData or FilterFormatMaskedAdData, outputDescription: FilterOutputDescription):
        self.type              = Uint8(type)
        self.profileId         = Uint8(profileId)
        self.input             = Uint8Array(input.getPacket())
        self.outputDescription = Uint8Array(outputDescription.getPacket())
