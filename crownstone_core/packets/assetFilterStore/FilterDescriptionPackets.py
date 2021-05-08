from enum import IntEnum
from crownstone_core.util.BasePackets import PacketBase, Uint8, Uint16, CsUint8Enum

class FilterType(CsUint8Enum):
    CUCKOO = 0

class AdvertisementSubdataType(CsUint8Enum):
    """
    Describes a selection of data from an advertisement.

    ASSET_FILTER_STORE.md#advertisement-subdata-type
    """
    MAC_ADDRESS    = 0
    AD_DATA        = 1
    MASKED_AD_DATA = 2

class FilterOutputDescription(CsUint8Enum):
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
        self.filterType = Uint8()
        self.filterCrc = Uint16()