from crownstone_core.util.BasePackets import *
from crownstone_core.packets.assetFilterStore.FilterDescriptionPackets import *


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
                                    type_getter_lambda = lambda: self.type
        )


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
    typeMap = {FilterOutputDescription.MAC_ADDRESS : FilterFormatMacAddress,
                        FilterOutputDescription.SHORT_ASSET_ID : FilterFormatAdData}

    def __init__(self):
        self.out_format = AdvertisementSubdataDescription()
        self.in_format = PacketVariant(type_enum_to_type_dict = FilterOutputDescription.typeMap,
                                       type_getter_lambda = lambda: self.out_format.type)




# class AdvertisementSubdataDescription_old(PacketBase):
#     """
#     ASSET_FILTER_STORE.md#advertisement-subdata-type
#     """
#     formatPacketMap = {AdvertisementSubdataDescription.MAC_ADDRESS : FilterFormatMacAddress,
#                        AdvertisementSubdataDescription.AD_DATA : FilterFormatAdData,
#                        AdvertisementSubdataDescription.MASKED_AD_DATA : FilterFormatMaskedAdData}
#
#     def __init__(self, subdatatype = None):
#         """
#         If default constructed (or with None parameter) the format member will be left unconstructed
#         so that the calling scope can decide what type to use. Otherwise 'format' will be a default
#         constructed object of the type for the given output_type.
#         """
#         self.type = Uint8()
#         self.format = None
#
#         if output_type is not None:
#             self.type = subdatatype
#             self.format = AdvertisementSubdataDescription.formatPacketMap[subdatatype]()



# class FilterOutputDescription(PacketBase):
#     """
#     ASSET_FILTER_STORE.md#filter-output-description
#     """
#     formatPacketMap = {FilterOutputDescription.MAC_ADDRESS : FilterFormatMacAddress,
#                         FilterOutputDescription.SHORT_ASSET_ID : FilterFormatAdData}
#
#     def __init__(self, subdatatype = None):
#         self.out_format = AdvertisementSubdataDescription(subdatatype)
#         self.in_format = None
#
#         if subdatatype is not None:
#             self.in_format = FilterOutputDescription.formatPacketMap[subdatatype]()