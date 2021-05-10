"""
This file contains helper functions for Bluenets TrackableParser component.
"""
from crownstone_core.util.CRC import crc16ccitt
from crownstone_core.util.Conversion import Conversion

def MasterCrc(listOfTrackingFilters):
    """
    Computes the master crc for the given a list of TrackingFilterData instances.
    The list of filters needs to be sorted by filter id.
    Does not warn for duplicate profile ids.
    """
    filterCrcs = map(
        lambda trackfilterdata: FilterCrc(trackfilterdata),
        listOfTrackingFilters
    )

    listFilterCrcs16 = list(filterCrcs)
    listFilterCrcs8 = Conversion.uint16_array_to_uint8_array(listFilterCrcs16)
    return crc16ccitt(listFilterCrcs8)

def FilterCrc(trackingFilter):
    return crc16ccitt(trackingFilter.getPacket())