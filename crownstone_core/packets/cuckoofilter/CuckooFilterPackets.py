from crownstone_core.packets.cuckoofilter.BasePackets import *


class CuckooExtendedFingerprint(PacketBase):
	def __init__(self):
		self.fingerprint = Uint16()
		self.bucketA = Uint8()
		self.bucketB = Uint8()


class CuckooFilterData(PacketBase):
	"""
	This corresponds to the cuckoo_filter_data_t on Bluenet.
	"""
	def __init__(self):
		self.bucketCountLog2 = Uint8()
		self.nestsPerBucket = Uint8()
		self.victim = CuckooExtendedFingerprint()
		self.bucketArray = Uint16Array()


class FilterInputType(CsUint8Enum):
	MacAddress = 0,
	AdData = 1,


class TrackingFilterMetaData(PacketBase) :
	def __init__(self):
		self.protocol = Uint8()
		self.version = Uint16()
		self.profileId = Uint8()
		self.inputType = FilterInputType.MacAddress
		self.flags = Uint8()


class TrackingFilterData(PacketBase):
	"""
	This packet is part of the tracking filter command protocol, where it is chunked to fit in <= MTU sized messages
	"""
	def __init__(self):
		self.metadata = TrackingFilterMetaData()
		self.filter = CuckooFilterData()

