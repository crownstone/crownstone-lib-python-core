from crownstone_core.util.Cuckoofilter import CuckooFilter
from crownstone_core.util.Conversion import Conversion

def test_add_contains():
    """
    Checks if
    _add(0), _add(1), ..., _add(max_items),
    _contains(0), _contains(1), ..., _contains(max_items),
    does what it 's supposed to do. A load factor is incorporated
    since cuckoo filters will not fit their theoretical max load.
    """

    # Settings for this test
    max_buckets_log2 = 7
    nests_per_bucket = 4
    load_factor = 0.75

    filter = CuckooFilter(max_buckets_log2, nests_per_bucket)

    # setup test variables
    max_items = filter.fingerprintcount()
    num_items_to_test = int(max_items * load_factor)
    fails = 0

    # Add a lot of integers
    for i in range(num_items_to_test):
        i_as_uint8_list = Conversion.uint32_to_uint8_array(i)
        if not filter.add(i_as_uint8_list):
            fails += 1

    assert fails == 0, "Add failed"
    fails = 0

    # check if they ended up in the filter
    for i in range(num_items_to_test):
        i_as_uint8_list = Conversion.uint32_to_uint8_array(i)
        if not filter.contains(i_as_uint8_list):
            fails += 1

    assert fails == 0, "Contains failed"
    fails = 0
