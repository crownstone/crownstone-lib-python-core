from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvAlternativeState:
    def __init__(self):
        self.type = AdvType.ALTERNATIVE_STATE

        self.crownstoneId        = None
        self.switchState         = None
        self.flags               = None
        self.behaviourMasterHash = None
        self.timestamp           = None
        self.uniqueIdentifier    = None
        self.validation          = None