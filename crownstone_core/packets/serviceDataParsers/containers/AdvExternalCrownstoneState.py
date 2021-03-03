from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvExternalCrownstoneState:
    def __init__(self):
        self.type = AdvType.EXTERNAL_STATE

        self.rssiOfExternalCrownstone  = None
        self.crownstoneId              = None
        self.switchState               = None
        self.flags                     = None
        self.temperature               = None
        self.powerFactor               = None
        self.powerUsageReal            = None
        self.powerUsageApparent        = None
        self.accumulatedEnergy         = None
        self.timestamp                 = None
        self.uniqueIdentifier          = None
        self.behaviourEnabled          = None
        self.validation                = None