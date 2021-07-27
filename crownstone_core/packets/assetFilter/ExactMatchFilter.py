from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.util.BufferWriter import BufferWriter

from crownstone_core.packets.assetFilter.AssetFilterPackets import FilterData


class ExactMatchFilter(FilterData):
    def __init__(self):
        self.itemCount = 0
        self.itemSize = 0
        self.items = []

    def add(self, item: list):
        """
        Add an item to the filter.

        @param item: Byte array representation of the item.
        """
        if self.itemCount:
            if self.itemSize != len(item):
                raise CrownstoneException(CrownstoneError.INVALID_SIZE, f"Must be same size as other items ({self.itemSize})")
        else:
            self.itemSize = len(item)
        self.items.append(item)
        self.itemCount = len(self.items)

    def _toBuffer(self, writer: BufferWriter):
        writer.putUInt8(self.itemCount)
        writer.putUInt8(self.itemSize)
        self.items.sort()
        for item in self.items:
            writer.putBytes(item)

    def __str__(self):
        return f"ExactMatchFilter(" \
               f"itemCount={self.itemCount} " \
               f"itemSize={self.itemSize} " \
               f"items={self.items})"