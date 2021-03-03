from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvExternalErrorPacket:
    def __init__(self):
        self.type = AdvType.EXTERNAL_ERROR

        self.crownstoneId              = None
        self.errorsBitmask             = None
        self.errorTimestamp            = None
        self.flags                     = None
        self.temperature               = None
        self.timestamp                 = None
        self.uniqueIdentifier          = None
        self.rssiOfExternalCrownstone  = None
        self.validation                = None