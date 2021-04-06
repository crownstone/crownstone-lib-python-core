from crownstone_core.util.BasePackets import *


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