from crownstone_core.util.BasePackets import *
from crownstone_core.packets.assetFilter.FilterDescriptionPackets import *


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
    def __init__(self):
        self.adType = Uint8()


class FilterFormatMaskedAdData(PacketBase):
    """
    FilterInputType.MASKED_AD_DATA
    """
    def __init__(self):
        self.adType = Uint8()
        self.mask   = Uint32()


class AdvertisementSubdata(PacketBase):
    """
    ASSET_FILTER_STORE.md#advertisement-subdata-description
    """
    typeMap = {
            AdvertisementSubdataType.MAC_ADDRESS : FilterFormatMacAddress,
            AdvertisementSubdataType.AD_DATA : FilterFormatAdData,
            AdvertisementSubdataType.MASKED_AD_DATA : FilterFormatMaskedAdData}

    def __init__(self):
        self.type = AdvertisementSubdataType.MAC_ADDRESS
        self.format = PacketVariant(type_enum_to_type_dict = AdvertisementSubdata.typeMap,
                                    type_getter_lambda = lambda: self.type)


class FilterInputDescription(PacketBase):
    """
    ASSET_FILTER_STORE.md#filter-input-description
    """
    def __init__(self):
        self.format = AdvertisementSubdata()


class FilterOutputDescription(PacketBase):
    """
    ASSET_FILTER_STORE.md#filter-output-description
    """
    typeMap = {FilterOutputFormat.MAC_ADDRESS : type(None),
               FilterOutputFormat.SHORT_ASSET_ID : AdvertisementSubdata}

    def __init__(self):
        self.out_format = FilterOutputFormat.MAC_ADDRESS
        self.in_format = PacketVariant(type_enum_to_type_dict = FilterOutputDescription.typeMap,
                                       type_getter_lambda = lambda: self.out_format.type)
