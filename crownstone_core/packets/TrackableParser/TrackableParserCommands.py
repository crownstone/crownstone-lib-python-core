from crownstone_core.util.BasePackets import *

# ------------------ Command packets ------------------

class UploadFilterCommandPacket(PacketBase):
	"""
	 Packet definition for ControlType.TRACKABLE_PARSER_REMOVE_FILTER
	"""
	def __init__(self):
		self.filterId = Uint8()
		self.chunkStartIndex = Uint16()
		self.totalSize = Uint16()
		self.chunkSize = Uint16() # @Bart: is this chunk size necessary or can it be computed upon reception?
		self.chunk = Uint8Array()

class RemoveFilterCommandPacket(PacketBase):
	"""
	 Packet definition for ControlType.TRACKABLE_PARSER_REMOVE_FILTER
	"""
	def __init__(self, filterId = None):
		self.filterId = Uint8(filterId if filterId is not None else 0)


class CommitFilterChangesCommandPacket(PacketBase):
	"""
	 Packet definition for ControlType.TRACKABLE_PARSER_COMMIT_CHANGES
	"""
	def __init__(self):
		self.masterVersion = Uint16()
		self.masterCrc = Uint16()

class GetFilterSummariesCommandPacket(PacketBase):
	"""
	 Packet definition for ControlType.TRACKABLE_PARSER_GET_SUMMARIES
	"""
	pass


# ------------------ Return values ------------------


class UploadFilterReturnPacket(PacketBase):
	pass


class RemoveFilterReturnPacket(PacketBase):
	pass


class CommitFilterChangesReturnPacket(PacketBase):
	pass


class GetFilterSummariesReturnPacket(PacketBase):
	pass
