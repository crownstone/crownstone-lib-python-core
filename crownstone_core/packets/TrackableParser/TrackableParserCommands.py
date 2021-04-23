from crownstone_core.util.BasePackets import *
from crownstone_core.packets.TrackableParser.TrackableParserPackets import TrackingFilterSummary

# ------------------ command wrapper packet ------------------
class TrackableParserCommandWrapper(PacketBase):
	"""
	Packet definition for trackable parser command wrapper.
	Construct using one of the command packets as argument,
	possibly a default constructed one E.g.:

	packet = UploadFilterCommandPacket()
	wrap = trackableParserCommandWrapper(packet)
	"""
	def __init__(self, commandpacket):
		self.commandProtocolVersion = Uint8()
		self.payload = commandpacket

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
	"""
	Definition of return packet ControlType.TRACKABLE_PARSER_GET_SUMMARIES
	"""
	def __init__(self):
		self.masterVersion = Uint16()
		self.masterCrc = Uint16()
		self.freeSpace = Uint16()
		self.summaries = PacketBaseList(cls=TrackingFilterSummary)
