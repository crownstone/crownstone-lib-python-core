from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvHubState:
    def __init__(self):
        self.type = AdvType.HUB_STATE

        self.crownstoneId     = None
        self.hubFlags         = None
        self.hubData          = None
        self.timestamp        = None
        self.validation       = None
        self.uniqueIdentifier = None
