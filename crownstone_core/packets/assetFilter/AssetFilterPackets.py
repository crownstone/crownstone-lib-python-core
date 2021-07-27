from crownstone_core.packets.assetFilter.CuckooFilterPackets import CuckooFilterData
from crownstone_core.packets.assetFilter.ExactMatchFilter import ExactMatchFilter
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *
from crownstone_core.packets.assetFilter.FilterOutputPackets import FilterOutputDescription
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.Bitmasks import set_bit


class FilterType(IntEnum):
    CUCKOO = 0
    EXACT_MATCH = 1



class FilterFlags(BasePacket):
    def __init__(self, exclude = False):
        self.exclude: bool = exclude
        self.bitmask: int  = 0
        self._calc_bitmask()

    def _calc_bitmask(self):
        self.bitmask = set_bit(self.bitmask, 0, self.exclude)

    def _toBuffer(self, writer: BufferWriter):
        self._calc_bitmask()
        writer.putUInt8(self.bitmask)

    def __str__(self):
        return f"FilterFlags(" \
               f"exclude={self.exclude})"



class FilterMetaData(BasePacket):
    """
    Common metadata of an asset filter.
    """
    def __init__(self,
                 type: FilterType,
                 filterInput: InputDescriptionMacAddress or InputDescriptionFullAdData or InputDescriptionMaskedAdData,
                 filterOutput: FilterOutputDescription,
                 profileId: int = 255,
                 flags: FilterFlags = FilterFlags()):
        self.type              = type
        self.flags             = flags
        self.profileId         = profileId
        self.filterInput       = filterInput
        self.filterOutput      = filterOutput

    def _toBuffer(self, writer: BufferWriter):
        writer.putUInt8(self.type)
        self.flags.toBuffer(writer)
        writer.putUInt8(self.profileId)
        self.filterInput.toBuffer(writer)
        self.filterOutput.toBuffer(writer)

    def __str__(self):
        return f"FilterMetaData(" \
               f"type={self.type} " \
               f"flags={self.flags} "\
               f"profileId={self.profileId} " \
               f"filterInput={self.filterInput} " \
               f"filterOutput={self.filterOutput})"



class FilterData(BasePacket):
    """
    Base class for filter data.
    """
    pass



class AssetFilter(BasePacket):
    """
    This is the packet that is uploaded.
    """
    def __init__(self,
                 metaData: FilterMetaData,
                 filterData: CuckooFilterData or ExactMatchFilter):
        self.metaData = metaData
        self.filterData = filterData

    def _toBuffer(self, writer: BufferWriter):
        self.metaData.toBuffer(writer)
        self.filterData.toBuffer(writer)

    def __str__(self):
        return f"AssetFilter(" \
               f"metaData={self.metaData} " \
               f"filterData={self.filterData})"



class AssetFilterAndId:
    def __init__(self, filterId: int, filter: AssetFilter):
        self.id = filterId
        self.filter = filter
