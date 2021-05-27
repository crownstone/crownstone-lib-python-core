from crownstone_core.util.BasePackets import *


class ExactMatchFilterData(PacketBase):
    def __init__(self):
        self.itemCount = Uint8()
        self.itemSize = Uint8()
        self.itemArray = PacketBaseList(cls=Uint8)