from crownstone_core.util.Cuckoofilter import CuckooFilter
from crownstone_core.util.Randomgenerator import RandomGenerator

def CheckTolerance(fails, total, tolerance):
    fails_rel = fails / total
    return not fails_rel > tolerance

def random_string(length, rand = RandomGenerator()):
    """
    Hoping that a tuple will not break any underlying code...
    """
    chrs = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".encode("utf-8")
    len_chrs = len(chrs)

    return tuple(chrs[rand() % len_chrs] for i in range(length))

def get_random_mac_address(rand):
    """
    Insert an instance of the MSWS rand generator
    """
    mac = []
    for i in range(0,6):
        mac.append(rand() % 256)
    return mac


def test_false_positive_rate():
    """
    Adds load_factor random entries to a filter and check if false positive rate stays below reasonable bounds.
    """
    # Settings for this test
    max_buckets_log2 = 7
    nests_per_bucket = 4
    load_factor = 0.95

    filter = CuckooFilter(max_buckets_log2, nests_per_bucket)
    
    # setup test variables
    max_items = filter.fingerprintcount()
    num_items_to_load = int(max_items * load_factor)
    assert num_items_to_load == 486, "test configuration has been altered"
    fails = 0
    
    # generate a bunch of random strings
    my_mac_passlist = []
    random_mac_addresses = []

    # this generator will ensure that the test is repeatable
    rand = RandomGenerator()

    for i in range(int(num_items_to_load)):
        my_mac_passlist.append(get_random_mac_address(rand))
        random_mac_addresses.append(get_random_mac_address(rand))

    # add the pass listed items to the filter
    for mac in my_mac_passlist:
        if not filter.add(mac):
            fails+= 1

    assert fails == 0, "Adding fails for given load_factor ({0:.1}%)".format(100*load_factor)
    fails = 0
    
    # check if all the passlisted items pass the filter
    for mac in my_mac_passlist:
        if not filter.contains(mac):
            fails+= 1

    assert fails == 0, "Contains incorrect after filling filter up to load_factor ({0:.1}%)".format(100 * load_factor)
    fails = 0

    # check if the random ones fail to pass the passlist
    # (unless they happen to be in there)
    false_positives = 0
    false_negatives = 0
    for mac in random_mac_addresses:
        should_contain = mac in my_mac_passlist
        filter_contains = filter.contains(mac)

        if filter_contains != should_contain:
            fails+= 1
            if filter_contains:
                false_positives += 1
            else:
                false_negatives += 1

    assert CheckTolerance(false_negatives, len(random_mac_addresses), 0.00), "False negatives should not occur"
    assert CheckTolerance(false_positives, len(random_mac_addresses), 0.05), "False positive rate too high"