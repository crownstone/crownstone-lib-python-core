from typing import List

from crownstone_core.Exceptions import CrownstoneException, CrownstoneError

from crownstone_core.util.Conversion import Conversion

from crownstone_core.packets.assetFilter.InputDescriptionPackets import *

from crownstone_core.packets.assetFilter.AssetFilterPackets import AssetFilter, AssetFilterAndId
from crownstone_core.packets.assetFilter.FilterCommandPackets import UploadFilterChunkPacket
from crownstone_core.util.Bitmasks import set_bit, get_bitmask
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.CRC import crc32
import math

class AssetFilterBuilder:
    def __init__(self):
        self.input: InputDescriptionPacket = None
        self.assets = []

    def filterByMacAddress(self, macAddresses: List[str]):
        """
        Assets are filtered by their MAC address.
        @param macAddresses: List of mac addresses to be added to the filter.
        """
        self.input = InputDescriptionMacAddress()
        self.assets = []
        for mac in macAddresses:
            self.assets.append(Conversion.address_to_uint8_array(mac))

    def filterByName(self, names: List[str], complete: bool = True):
        """
        Assets are filtered by their name.
        @param names:     List of names to be added filter.
        @param complete:  Whether to look for the complete or shortened name.
        """
        adType = 0x09 if complete else 0x08
        self.input = InputDescriptionFullAdData(adType)

        self.assets = []
        for name in names:
            self.assets.append(Conversion.string_to_uint8_array(name))

    def filterByNameWithWildcards(self, name: str, complete: bool = True):
        """
        Assets are filtered by their name.
        @param name:      Name, with wildcards, to be added filter.
                          '?' matches any single character
                          '*' matches zero or more characters, only at the end of a name.
                          Example: "??_dev*" will match:  "my_dev", and "01_device"
                                             won't match: "your_device", or "_dev"
        @param complete:  Whether to look for the complete or shortened name.
        """
        if len(name) > 31:
            raise CrownstoneException(CrownstoneError.INVALID_SIZE, f"Name is too long: {name}")
        bitmask = 0
        asset_name = ""
        for i in range(0, len(name)):
            if name[i] != '?':
                set_bit(bitmask, i)
                asset_name += name[i]
        if name[-1] == '*':
            set_bit(bitmask, len(name), False)
        else:
            # TODO: does this work?
            for i in range(len(name), 31):
                set_bit(bitmask, i)

        adType = 0x09 if complete else 0x08
        self.input = InputDescriptionMaskedAdData(adType, bitmask)
        self.assets = [asset_name]

    def filterByCompanyId(self, companyIds: List[int]):
        """
        Assets are filtered by their 16 bit company ID.
        @param companyId: The 16 bit company ID.
        """
        self.input = InputDescriptionMaskedAdData(0xFF, get_bitmask([0,1]))
        self.assets = []
        for companyId in companyIds:
            self.assets.append(Conversion.uint16_to_uint8_array(companyId))

    def filterByAdData(self, adType: int, assets: List[list], bitmask: int = None):
        """
        Assets are recognized by the data of a single AD structure in a BLE advertisement.
        @param adType:  The 8 bit GAP number.
        @param assets:  A list of assets, where each asset is represented by a list of bytes.
        @param bitmask: A bitmask where the Nth bit represents the Nth byte in the AD data.
                        The data that is used as input for the filter, is a concatenation of all bytes that have their
                        associated bit set.
                        Example: if the AD data is: [10, 11, 12, 13, 14] and the bitmask is 22 (0000...00010110), then
                        the data that the filter uses is [11, 12, 14], and matched against each given asset.
        """
        if bitmask is None:
            self.input = InputDescriptionFullAdData(adType)
        else:
            self.input = InputDescriptionMaskedAdData(adType, bitmask)

def get_master_crc_from_filters(filters: [AssetFilterAndId]) -> int:
    input_data = []
    for filter in filters:
        id = filter.id
        crc = get_filter_crc(filter.filter)
        input_data.append([id, crc])
    return get_master_crc_from_filter_crcs(input_data)

def get_master_crc_from_filter_crcs(input_data : [[int, int]]) -> int:
    """
        the input data is an array of [filterId, filterCRC] numbers
        This method is used to get the masterCRC
    """
    def sort_method(val):
        return val[0]

    input_data.sort(key=sort_method)
    writer = BufferWriter()

    for id_and_filter_crc in input_data:
        writer.putUInt8(id_and_filter_crc[0])
        writer.putUInt32(id_and_filter_crc[1]) # TODO: use packets to serialize.

    return crc32(writer.getBuffer())

def get_filter_crc(filter: AssetFilter) -> int:
    """
    """
    return crc32(filter.toBuffer())

class FilterChunker:

    def __init__(self, filterId: int, filterPacket: [int], maxChunkSize=128):
        self.filterId = filterId
        self.filterPacket = filterPacket

        self.index = 0
        self.maxChunkSize = maxChunkSize

    def getAmountOfChunks(self) -> int:
        totalSize = len(self.filterPacket)
        count = math.floor(totalSize/self.maxChunkSize)
        if totalSize % self.maxChunkSize > 0:
            count += 1
        return count

    def getChunk(self) -> [int]:
        totalSize = len(self.filterPacket)
        if totalSize > self.maxChunkSize:
            chunkSize = min(self.maxChunkSize, totalSize - self.index)
            chunkData = self.filterPacket[self.index : self.index + chunkSize]
            cmd = UploadFilterChunkPacket(self.filterId, self.index, totalSize, chunkSize, chunkData)
            self.index += self.maxChunkSize
            return cmd.toBuffer()
        else:
            return UploadFilterChunkPacket(self.filterId, self.index, totalSize, totalSize, self.filterPacket).toBuffer()


