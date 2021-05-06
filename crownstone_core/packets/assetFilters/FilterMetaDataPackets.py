from crownstone_core.util.BasePackets import PacketBase, Uint8, Uint16, CsUint8Enum, Uint32, Uint8Array
from crownstone_core.packets.assetFilters.FilterTypes import FilterInputType


class FilterMetaData(PacketBase):

    def __init__(self):
        self.type              = Uint8()
        self.profileId         = Uint8()
        self.input             = Uint8Array()
        self.outputDescription = Uint8Array()

class FilterFormatMacAddress(PacketBase):

    def __init__(self):
        self.type = Uint8(FilterInputType.MAC_ADDRESS)


class FilterFormatAdData(PacketBase):

    def __init__(self, adType: int):
        self.type   = Uint8(FilterInputType.AD_DATA)
        self.adType = Uint8(adType)


class FilterFormatMaskedAdData(PacketBase):

    def __init__(self, adType: int, mask: int):
        self.type   = Uint8(FilterInputType.MASKED_AD_DATA)
        self.adType = Uint8(adType)
        self.mask   = Uint32(mask)


class FilterOutputDescription(PacketBase):

    def __init__(self, output_type: int, formatPacket : FilterFormatMacAddress or FilterFormatMacAddress or FilterFormatMaskedAdData = None):
        self.type = Uint8(output_type)
        if formatPacket is not None:
            self.format = Uint8Array(formatPacket.getPacket())
