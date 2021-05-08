from crownstone_core.util.BasePackets import *
# from crownstone_core.packets.TrackableParser.TrackableParserPackets import TrackingFilterSummary


# ------------------ TRACKABLE_PARSER.md#trackable-parser-protocol-version ------------------

ASSET_FILTER_PROTOCOL = Uint8(0)

# ------------------ TRACKABLE_PARSER.md#upload-filter ------------------

class UploadFilterCommandPacket(PacketBase):
    """
    Packet definition for ControlType.TRACKABLE_PARSER_REMOVE_FILTER
    """

    def __init__(self):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.filterId = Uint8()
        self.chunkStartIndex = Uint16()
        self.totalSize = Uint16()
        self.chunkSize = Uint16()
        self.chunk = Uint8Array()

# ------------------ TRACKABLE_PARSER.md#remove-filter  ------------------

class RemoveFilterCommandPacket(PacketBase):
    """
     Packet definition for ControlType.TRACKABLE_PARSER_REMOVE_FILTER
    """

    def __init__(self, filterId=None):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.filterId = Uint8(filterId if filterId is not None else 0)

# ------------------ TRACKABLE_PARSER.md#commit-filter-changes  ------------------

class CommitFilterChangesCommandPacket(PacketBase):
    """
     Packet definition for ControlType.TRACKABLE_PARSER_COMMIT_CHANGES
    """

    def __init__(self):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.masterVersion = Uint16()
        self.masterCrc = Uint16()

# ------------------ TRACKABLE_PARSER.md#get-filter-summaries ------------------

class GetFilterSummariesReturnPacket(PacketBase):
    """
    Definition of return packet ControlType.TRACKABLE_PARSER_GET_SUMMARIES
    """
    def __init__(self):
        self.commandProtocolVersion = Uint8()
        self.masterVersion = Uint16()
        self.masterCrc = Uint16()
        self.freeSpace = Uint16()
        self.summaries = PacketBaseList(cls=TrackingFilterSummary)
