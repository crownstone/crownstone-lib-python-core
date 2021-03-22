from py.cuckoofilter import CuckooFilter
from py.randomgenerator import RandomGenerator
from crownstone_core.util.Conversion import Conversion
from colorama import Fore, Back, Style


def Status(fails):
    if fails:
        return "{0}[FAIL]{1} ({2})".format(Style.BRIGHT + Fore.RED, Style.RESET_ALL, fails)
    else:
        return "{0}[OK]{1}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL)


def StatusRelative(fails, total, tolerance):
    fails_rel = fails / total
    fail = fails_rel > tolerance

    return "{0} {1} {2} {3}".format(
        Style.BRIGHT + Fore.RED if fail else Style.BRIGHT + Fore.GREEN,
        "[FAIL]" if fail else "[OK]",
        Style.RESET_ALL,
        "{0:.2f}%".format(100*fails_rel)
    )


def random_string(length, rand = RandomGenerator()):
    """
    Hoping that a tuple will not break any underlying code...
    """
    chrs = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".encode("utf-8")
    len_chrs = len(chrs)

    return tuple(chrs[rand() % len_chrs] for i in range(length))


# Allocates FILTER_COUNT filters, then adds the same sequence to each,
# tests if this sequence is passes containment check and frees the filters.
#
if __name__ == "__main__":
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

    print("ADD 0: ", Status(fails))
    fails = 0
    
    # check if all the passlisted items pass the filter
    for mac in my_mac_passlist:
        if not filter.contains(mac):
            fails+= 1
    
    print("CONTAINS 0: ", Status(fails))
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

    print("CONTAINS false negatives ",
          StatusRelative(false_negatives, len(random_mac_addresses), 0.00),
          "total: {0} / {1}.".format(false_negatives, len(random_mac_addresses)))
    print("CONTAINS false positives ",
          StatusRelative(false_positives, len(random_mac_addresses), 0.05),
          "total: {0} / {1}.".format(false_positives, len(random_mac_addresses)))
