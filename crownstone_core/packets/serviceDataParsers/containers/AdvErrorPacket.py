from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvErrorPacket:
    def __init__(self):
        self.type = AdvType.CROWNSTONE_ERROR

        self.crownstoneId              = None
        self.errorsBitmask             = None
        self.errorTimestamp            = None
        self.flags                     = None
        self.temperature               = None
        self.timestamp                 = None
        self.uniqueIdentifier          = None
        self.powerUsageReal            = None
