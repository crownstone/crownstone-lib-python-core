from crownstone_core.packets.TrackableParser.TrackableParserPacketsUtil import PacketBase, Uint8, Uint16, Uint8Array, Uint16Array, CsEnum8

class FilterInputType(CsEnum8):
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


class CuckooFilterData(PacketBase):
    def __init__(self):
        self.bucket_count = Uint8()
        self.nests_per_bucket = Uint8()
        self.victim_fingerprint = Uint16()
        self.victim_bucketA = Uint8()
        self.victim_bucketB = Uint8()
        self.fingerprintarray = Uint16Array()

class TrackingFilterData(PacketBase):
    def __init__(self):
        self.metadata = TrackingFilterMetaData()
        self.filter = CuckooFilterData()


class TrackingFilterUpload(PacketBase):
    """
     Packet definition for command upload filter.

    """
    def __init__(self):
        self.filterId = Uint8()
        self.chunkStartIndex = Uint16()
        self.totalSize = Uint16()
        self.chunkSize = Uint16() # @Bart: is this chunk size necessary or can it be computed upon reception?
        self.chunk = Uint8Array()
