from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvCrownstoneSetupState:
    def __init__(self):
        self.type = AdvType.SETUP_STATE

        self.switchState               = None
        self.flags                     = None
        self.temperature               = None
        self.powerFactor               = None
        self.powerUsageReal            = None
        self.powerUsageApparent        = None
        self.errorBitmask              = None
        self.uniqueIdentifier          = None