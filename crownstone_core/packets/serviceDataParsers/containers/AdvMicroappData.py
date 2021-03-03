from crownstone_core.packets.serviceDataParsers.containers.AdvTypes import AdvType


class AdvMicroappData:
    def __init__(self):
        self.type = AdvType.MICROAPP_DATA

        self.microappUuid     = None
        self.microappData     = None
        self.crownstoneId     = None
        self.validation       = None
        self.uniqueIdentifier = None
        self.flags            = None