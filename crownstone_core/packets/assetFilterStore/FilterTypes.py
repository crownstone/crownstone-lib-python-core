from enum import IntEnum

class FilterType(IntEnum):
    CUCKOO = 0

class AdvertisementSubdataDescription(IntEnum):
    """
    Describes a selection of data from an advertisement.

    ASSET_FILTER_STORE.md#advertisement-subdata-type
    """
    MAC_ADDRESS    = 0
    AD_DATA        = 1
    MASKED_AD_DATA = 2

class FilterOutputDescription(IntEnum):
    """
    ASSET_FILTER_STORE.md#filter-output-format
    """
    MAC_ADDRESS = 0
    SHORT_ASSET_ID = 1