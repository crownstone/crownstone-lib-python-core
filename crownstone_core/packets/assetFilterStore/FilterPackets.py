import math

from crownstone_core.util.BasePackets import *

# This will be changed once we actually support 2 different protocol versions.

class TrackingFilterData(PacketBase):
    """
    ASSET_FILTER_STORE.md#tracking-filter-data
    This packet is part of the tracking filter command protocol, where it is chunked to fit in <= MTU sized messages
    """
    def __init__(self):
        self.metadata = TrackingFilterMetaData()
        self.filter = Uint8Array() # CuckooFilterData()



class FilterSummary(PacketBase):
    """
    ASSET_FILTER_STORE.md#filter-summary
    """
    def __init__(self):
        self.filterId   = Uint8()
        self.filterType = Uint8()
        self.filterCrc  = Uint16()
