from enum import IntEnum
from crownstone_core.util.BasePackets import PacketBase, Uint8, Uint32, CsUint8Enum

"""
TODO: rename packets
TODO: add constructors
"""

class FilterType(CsUint8Enum):
    CUCKOO = 0
    EXACT_MATCH = 1

class AdvertisementSubdataType(CsUint8Enum):
    """
    Describes a selection of data from an advertisement.

    ASSET_FILTER_STORE.md#advertisement-subdata-type
    """
    MAC_ADDRESS    = 0
    AD_DATA        = 1
    MASKED_AD_DATA = 2

class FilterOutputFormat(CsUint8Enum):
    """
    ASSET_FILTER_STORE.md#filter-output-format
    """
    MAC_ADDRESS = 0
    SHORT_ASSET_ID = 1

class FilterSummary(PacketBase):
    """
    ASSET_FILTER_STORE.md#filter-summary
    """
    def __init__(self):
        self.filterId = Uint8()
        self.filterCrc = Uint32()