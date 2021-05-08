from crownstone_core.util.BasePackets import *

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
    ASSET_FILTER_STORE.md#advertisement-subdata-type
    """
    def __init__(self, output_type: int, formatPacket : FilterFormatMacAddress or FilterFormatMacAddress or FilterFormatMaskedAdData = None):
        self.type = Uint8(output_type)
        if formatPacket is not None:
            self.format = Uint8Array(formatPacket.getPacket())





