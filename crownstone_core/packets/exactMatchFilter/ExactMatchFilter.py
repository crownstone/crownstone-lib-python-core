from crownstone_core.util.BasePackets import *


class ExactMatchFilterData(PacketBase):
    def __init__(self, itemCount=None, itemSize=None):
        self.itemCount = Uint8(itemCount)
        self.itemSize = Uint8(itemSize)
        self.itemArray = PacketBaseList(cls=Uint8)