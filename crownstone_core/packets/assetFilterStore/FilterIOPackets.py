from crownstone_core.packets.assetFilterStore.FilterDescriptionPackets import AdvertisementSubdataDescription
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
    formatPacketMap = {AdvertisementSubdataDescription.MAC_ADDRESS : FilterFormatMacAddress,
                       AdvertisementSubdataDescription.AD_DATA : FilterFormatAdData,
                       AdvertisementSubdataDescription.MASKED_AD_DATA : FilterFormatMaskedAdData}

    def __init__(self, output_type = None):
        """
        If default constructed (or with None parameter) the format member will be left unconstructed
        so that the calling scope can decide what type to use. Otherwise 'format' will be a default
        constructed object of the type for the given output_type.
        """
        self.type = Uint8()
        self.format = None

        if output_type is not None:
            self.type = output_type
            self.format = FilterOutputDescription.formatPacketMap[output_type]()





