import logging
import math
from typing import List

from crownstone_core import Conversion
from crownstone_core.Exceptions import CrownstoneException, CrownstoneError
from crownstone_core.util.Bitmasks import set_bit, get_bitmask

from crownstone_core.util.Cuckoofilter import CuckooFilter

from crownstone_core.packets.assetFilter.AssetFilterPackets import AssetFilter
from crownstone_core.packets.assetFilter.ExactMatchFilter import ExactMatchFilter
from crownstone_core.packets.assetFilter.FilterOutputPackets import FilterOutputDescriptionType, FilterOutputDescription
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *
from crownstone_core.packets.assetFilter.FilterMetaDataPackets import FilterType, FilterMetaData, FilterFlags
from crownstone_core.packets.assetFilter.builders.AssetIdBuilder import AssetIdBuilder

_LOGGER = logging.getLogger(__name__)

class AssetFilterBuilder:
    """
    Class that helps to build an asset filter.
    1. Choose what to filter by:       filterByX()
    2. Optionally, set configurations: setX()
    3. Choose the output:              outputX()
    4. Build to get an asset filter:   build()
    """
    def __init__(self):
        self.filterType: FilterType = None
        self.input: InputDescriptionPacket = None
        # self.output: FilterOutputDescription = None
        self.outputType: FilterOutputDescriptionType = None
        self.assetIdBuilder: AssetIdBuilder = None
        self.assets = []
        self.profileId = 255
        self.exclude = False

    def build(self) -> AssetFilter:
        # Build output
        if self.exclude:
            output = FilterOutputDescription(FilterOutputDescriptionType.MAC_ADDRESS, InputDescriptionMacAddress())
        else:
            output = None
            if self.outputType == FilterOutputDescriptionType.MAC_ADDRESS:
                output = FilterOutputDescription(FilterOutputDescriptionType.MAC_ADDRESS, InputDescriptionMacAddress())
            elif self.outputType == FilterOutputDescriptionType.SHORT_ASSET_ID:
                output = FilterOutputDescription(FilterOutputDescriptionType.SHORT_ASSET_ID, self.assetIdBuilder.build())
            else:
                raise CrownstoneException(CrownstoneError.UNKNOWN_TYPE, f"Unkown or missing output type: {self.outputType}")

        # Determine filter type to use.
        if self.filterType is None:
            equalSize = True
            assetSize = len(self.assets[0])
            totalSize = 0
            for asset in self.assets:
                if len(asset) != assetSize:
                    equalSize = False
                totalSize += len(asset)
            _LOGGER.debug(f"equalSize={equalSize} totalSize={totalSize}")

            # TODO: 400 as max size is an estimate.
            if totalSize < 400 and equalSize:
                self.filterType = FilterType.EXACT_MATCH
            else:
                self.filterType = FilterType.CUCKOO

        # Build the meta data.
        metaData = FilterMetaData(self.filterType, self.input, output, self.profileId, FilterFlags(exclude=self.exclude))

        # Construct and fill the filter.
        if self.filterType == FilterType.EXACT_MATCH:
            filterData = ExactMatchFilter()
            for asset in self.assets:
                filterData.add(asset)
        elif self.filterType == FilterType.CUCKOO:
            # TODO: move this to cuckoo filter implementation.
            initialNestsPerBucket = 4
            requiredBucketCount = len(self.assets) / 0.95 / initialNestsPerBucket
            bucketCountLog2 = max(0, math.ceil(math.log2(requiredBucketCount)))
            bucketCount = math.pow(2, bucketCountLog2)
            nestsPerBucket = math.ceil(len(self.assets) / bucketCount)

            cuckooFilter = CuckooFilter(bucketCountLog2, nestsPerBucket)
            for asset in self.assets:
                if not cuckooFilter.add(asset):
                    raise CrownstoneException(CrownstoneError.INVALID_SIZE, "Failed to add asset to cuckoo filter.")
            filterData = cuckooFilter.getData()

        return AssetFilter(metaData, filterData)


    def filterByMacAddress(self, macAddresses: List[str]):
        """
        Assets are filtered by their MAC address.
        :param macAddresses: List of mac addresses to be added to the filter, in the form of "12:34:56:78:AB:CD".
        """
        self._checkInputExists()

        self.input = InputDescriptionMacAddress()
        self.assets = []
        for mac in macAddresses:
            self.assets.append(Conversion.address_to_uint8_array(mac))
        return self

    def filterByName(self, names: List[str], complete: bool = True):
        """
        Assets are filtered by their name.
        :param names:     List of names to be added filter.
        :param complete:  Whether to look for the complete or shortened name.
        """
        self._checkInputExists()

        adType = 0x09 if complete else 0x08
        self.input = InputDescriptionFullAdData(adType)

        self.assets = []
        for name in names:
            self.assets.append(Conversion.string_to_uint8_array(name))
        return self

    def filterByNameWithWildcards(self, name: str, complete: bool = True):
        """
        Assets are filtered by their name.
        :param name:      Name, with wildcards, to be added filter.
                          '?' matches any single character
                          '*' matches zero or more characters, only at the end of a name.
                          Example: "??_dev*" will match:  "my_dev", and "01_device"
                                             won't match: "your_device", or "_dev"
        :param complete:  Whether to look for the complete or shortened name.
        """
        self._checkInputExists()

        if len(name) > 31:
            raise CrownstoneException(CrownstoneError.INVALID_SIZE, f"Name is too long: {name}")
        bitmask = 0
        asset_name = ""
        for i in range(0, len(name)):
            if name[i] != '?':
                bitmask = set_bit(bitmask, i)
                asset_name += name[i]
        if name[-1] == '*':
            bitmask = set_bit(bitmask, len(name) - 1, False)
        else:
            # TODO: does this work?
            for i in range(len(name), 32):
                bitmask = set_bit(bitmask, i)

        _LOGGER.info(f"name={name} bitmask={bitmask:032b} asset_name={asset_name}")

        adType = 0x09 if complete else 0x08
        self.input = InputDescriptionMaskedAdData(adType, bitmask)
        self.assets = [Conversion.string_to_uint8_array(asset_name)]
        return self

    def filterByCompanyId(self, companyIds: List[int]):
        """
        Assets are filtered by their 16 bit company ID.
        :param companyIds: A list of 16 bit company IDs. As can be found on
                           https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/
        """
        self._checkInputExists()

        self.input = InputDescriptionMaskedAdData(0xFF, get_bitmask([0,1]))
        self.assets = []
        for companyId in companyIds:
            self.assets.append(Conversion.uint16_to_uint8_array(companyId))
        return self

    def filterByAdData(self, adType: int, assets: List[list], bitmask: int = None):
        """
        Assets are recognized by the data of a single AD structure in a BLE advertisement.
        :param adType:  The 8 bit GAP number.
                        See "Generic Access Profile" on https://www.bluetooth.com/specifications/assigned-numbers/
        :param assets:  A list of assets, where each asset is represented by a list of bytes.
        :param bitmask: A 32 bits mask where the Nth bit represents the Nth byte in the AD data.
                        The data that is used as input for the filter, is a concatenation of all bytes that have their
                        associated bit set.
                        Example: if the AD data is: [10, 11, 12, 13, 14] and the bitmask is 22 (0000...00010110), then
                        the data that the filter uses is [11, 12, 14], and matched against each given asset.
        """
        self._checkInputExists()

        if bitmask is None:
            self.input = InputDescriptionFullAdData(adType)
        else:
            self.input = InputDescriptionMaskedAdData(adType, bitmask)
        self.assets = assets
        return self


    def setFilterType(self, filterType: FilterType):
        """
        Set the filter type.

        Each filter type has its pros and cons:
        - Cuckoo: stores a list of 2 bytes hashes of the asset data. This means there can be false positives.
            Use this type when:
                - You have many asset entries, each more than 2B of data.
                - You have asset entries of varying length.
            Examples:
                - 50 MAC addresses.
                - 10 names of different length.
        - Exact match: stores a list of the whole asset data. It only accepts same length entries, and does not compress the data.
            Use this type when:
                - You have a few assets to add.
                - You do not want any false positives.
            Examples:
                - 10 MAC addresses.
                - A list of company IDs.
                - A name.
        """
        self.filterType = filterType
        return self

    def setExclude(self, exclude=True):
        """
        Make this an exclude filter.

        Any asset that passes an exclude filter, will be prevented from passing any other filter.
        An exclude filter has no output, so you don't have to choose one.

        :param exclude: True to make this an exclude filter.
        """
        self.exclude = exclude
        return self

    def setProfileId(self, profileId: int):
        """
        By setting a profile ID, any asset advertisement that passes this filter will be treated as this profile ID
        for behaviours. If the localization cannot determine which room the asset is in, it will be still be treated as
        being in the sphere.

        :param profileId:    The profile ID for behaviour. 255 for no profile ID.
        """
        self.profileId = profileId
        return self


    def outputMacRssiReport(self):
        """
        If an asset advertisement passes the filter, the Crownstone will send a report to the hub
        with the assets' MAC address and the RSSI.
        """
        self.outputType = FilterOutputDescriptionType.MAC_ADDRESS
        return self

    def outputAssetId(self, basedOn: AssetIdBuilder = None) -> AssetIdBuilder:
        """
        If an asset advertisement passes the filter, the Crownstones will attempt to localize it, and will identify it
        by a 3 byte asset ID. The asset ID is a hash over data from the advertisement, which can be different data than
        what it's filtered by. Select this data with the AssetIdBuilder.

        :param basedOn: Determines what data to base the short asset ID on.
        """
        self.outputType = FilterOutputDescriptionType.SHORT_ASSET_ID
        if basedOn is None:
            self.assetIdBuilder = AssetIdBuilder()
        else:
            self.assetIdBuilder = basedOn
        return self.assetIdBuilder


    def _checkInputExists(self):
        if self.input is not None:
            _LOGGER.info("Removing existing input and assets")