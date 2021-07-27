from enum import IntEnum

from crownstone_core.util.BufferWriter import BufferWriter

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *

class FilterOutputDescriptionType(IntEnum):
    """
    What type of message should be output.
    """
    MAC_ADDRESS = 0
    SHORT_ASSET_ID = 1

class FilterOutputDescription(BasePacket):
    def __init__(self,
                 outFormat: FilterOutputDescriptionType,
                 inFormat: InputDescriptionMacAddress or InputDescriptionFullAdData or InputDescriptionMaskedAdData):
        self.outFormat = outFormat
        self.inFormat  = inFormat

    def _toBuffer(self, writer: BufferWriter):
        writer.putUInt8(self.outFormat)
        self.inFormat.toBuffer(writer)

    def __str__(self):
        return f"FilterOutputDescription(" \
               f"inFormat={self.inFormat} " \
               f"outFormat={self.outFormat})"