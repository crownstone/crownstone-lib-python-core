from enum import IntEnum

class FilterType(IntEnum):
    CUCKOO_V1 = 0

class FilterInputType(IntEnum):
    MAC_ADDRESS    = 0
    AD_DATA        = 1
    MASKED_AD_DATA = 2

class FilterOutputDescriptionType(IntEnum):
    MAC_ADDRESS_REPORT   = 0
    SHORT_ASSET_ID_TRACK = 1