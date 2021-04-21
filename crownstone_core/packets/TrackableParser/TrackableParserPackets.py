from crownstone_core.util.BasePackets import PacketBase, Uint8, Uint16, CsUint8Enum
from crownstone_core.packets.cuckoofilter.CuckooFilterPackets import CuckooFilterData

class FilterInputType(CsUint8Enum):
    MacAddress = 0
    AdDataIdentity = 1
    AdDataCategory = 2


class TrackingFilterMetaData(PacketBase):
    def __init__(self):
        self.protocol = Uint8()
        self.version = Uint16()
        self.profileId = Uint8()
        self.inputType = FilterInputType.MacAddress
        self.flags = Uint8() # bitmask not implemented yet


class TrackingFilterData(PacketBase):
    """
    This packet is part of the tracking filter command protocol, where it is chunked to fit in <= MTU sized messages
    """
    def __init__(self):
        self.metadata = TrackingFilterMetaData()
        self.filter = CuckooFilterData()

class TrackingFilterSummary(PacketBase):
    def __init__(self):
        self.id = Uint8()
        self.flags = Uint8()
        self.version = Uint16()
        self.crc = Uint16()
