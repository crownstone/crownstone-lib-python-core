from crownstone_core.packets.assetFilter.AssetFilterPackets import AssetFilterPacket
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.util.CRC import crc32

class AssetFilterAndId:
    def __init__(self, filterId: int, filter: AssetFilterPacket):
        self.id = filterId
        self.filter = filter

def get_master_crc_from_filters(filters: [AssetFilterAndId]) -> int:
    """
    Get the master CRC from filter CRCs.

    :param filters:     A list of asset filters and their ID.
    :returns:           The master CRC.
    """
    input_data = []
    for filter in filters:
        id = filter.id
        crc = get_filter_crc(filter.filter)
        input_data.append([id, crc])
    return get_master_crc_from_filter_crcs(input_data)

def get_master_crc_from_filter_crcs(input_data : [[int, int]]) -> int:
    """
    Get the master CRC from filter CRCs.

    :param input_data:  A list of [filterId, filterCRC].
    :returns:           The master CRC.
    """
    def sort_method(val):
        return val[0]

    input_data.sort(key=sort_method)
    writer = BufferWriter()

    for id_and_filter_crc in input_data:
        writer.putUInt8(id_and_filter_crc[0])
        writer.putUInt32(id_and_filter_crc[1]) # TODO: use packets to serialize.

    return crc32(writer.getBuffer())

def get_filter_crc(filter: AssetFilterPacket) -> int:
    """
    Get the filter CRC.

    :param filter:      The asset filter.
    :returns:           The asset filter CRC.
    """
    return crc32(filter.toBuffer())
