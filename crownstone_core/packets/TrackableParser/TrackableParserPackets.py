from crownstone_core.packets.TrackableParser.TrackableParserPacketsUtil import PacketBase, Uint8, Uint16, Uint8Array, Uint16Array, CsEnum8

class FilterInputType(CsEnum8):
    MacAddress = 0
    AdData     = 1


class TrackingFilterMetaData(PacketBase):
    def __init__(self):
        self.protocol = Uint8()
        self.version = Uint16()
        self.profileId = Uint16()
        self.inputType = FilterInputType.MacAddress # must choose default value for IntEnum
        self.flags = Uint8() # bitmask not implemented yet


class CuckooPacket(PacketBase):
    def __init__(self, cuckoo = None):
        self.bucket_count = Uint8()
        self.nests_per_bucket = Uint8()
        self.victim_fingerprint = Uint16()
        self.victim_bucketA = Uint8()
        self.victim_bucketB = Uint8()
        self.fingerprintarray = Uint16Array()

        if cuckoo is not None:
            self.loadCuckooFilter(cuckoo)

    def loadCuckooFilter(self, cuckoo):
        self.bucket_count = cuckoo.bucket_count
        self.nests_per_bucket = cuckoo.nests_per_bucket
        self.victim_fingerprint = cuckoo.victim.fingerprint
        self.victim_bucketA = cuckoo.victim.bucketA
        self.victim_bucketB = cuckoo.victim.bucketB
        self.fingerprintarray = cuckoo.bucket_array


class TrackingFilterData(PacketBase):
    def __init__(self):
        self.metadata = TrackingFilterMetaData()
        self.filter = CuckooPacket()


class TrackingFilterUpload(PacketBase):
    def __init__(self):
        self.filterId = Uint8()
        self.chunkStartIndex = Uint16()
        self.totalSize = Uint16()
        self.chunkSize = Uint16()
        self.chunk = Uint8Array()
