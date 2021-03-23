from crownstone_core.util.cuckoofilter import CuckooFilter
from crownstone_core.util.randomgenerator import RandomGenerator

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


def test_false_positive_rate():
    """
    Adds load_factor random entries to a filter and check if false positive rate stays below reasonable bounds.
    """
    # Settings for this test
    max_buckets = 128
    nests_per_bucket = 4
    load_factor = 0.95

    filter = CuckooFilter(max_buckets, nests_per_bucket)
    
    # setup test variables
    max_items = max_buckets * nests_per_bucket
    num_items_to_test = int(max_items * load_factor)
    fails = 0
    
    # generate a bunch of random strings
    my_mac_passlist = []
    random_mac_addresses = []
    for i in range(int(num_items_to_test)):
        my_mac_passlist += [ random_string(6) ]
        random_mac_addresses += [ random_string(6) ]

    my_mac_passlist = set(my_mac_passlist)
    random_mac_addresses = set(random_mac_addresses)
    
    # add the passlisted items to the filter
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
