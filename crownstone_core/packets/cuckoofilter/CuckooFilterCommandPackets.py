from crownstone_core.packets.cuckoofilter.BasePackets import *

# ------------------ Command packets ------------------

class UploadFilterCommandPacket(PacketBase):
	def __init__(self):
		self.filterId = Uint8()
		self.chunkStartIndex = Uint16()
		self.totalSize = Uint16()
		self.chunkSize = Uint16()
		self.chunk = Uint8Array()

class RemoveFilterCommandPacket(PacketBase):
	def __init__(self):
		self.filterId = Uint8()


class CommitFilterChangesCommandPacket(PacketBase):
	def __init__(self):
		self.masterVersion = Uint16()
		self.masterCrc = Uint16()

class GetFilterSummariesCommandPacket(PacketBase):
	pass

# ------------------ Return values ------------------


class trackable_parser_cmd_upload_filter_ret :
	pass


class trackable_parser_cmd_remove_filter_ret :
	pass


class trackable_parser_cmd_commit_filter_changes_ret :
	pass


class trackable_parser_cmd_get_filer_summaries_ret :
	pass

