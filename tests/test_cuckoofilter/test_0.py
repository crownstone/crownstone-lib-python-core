from py.cuckoofilter import CuckooFilter
from crownstone_core.util.Conversion import Conversion
from colorama import Fore, Back, Style

def Status(fails):
    if fails > 0:
        return "{0}[FAIL]{1} ({2})".format(Style.BRIGHT + Fore.RED, Style.RESET_ALL, fails)
    else:
        return "{0}[OK]{1}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL)

def goodbad(good, message):
    if not good:
        return "{0}[{2}]{1}".format(Style.BRIGHT + Fore.RED, Style.RESET_ALL, message)
    else:
        return "{0}[{2}]{1}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, message)


# Checks if
# _add(0), _add(1), ..., _add(max_items),
# _contains(0), _contains(1), ..., _contains(max_items),
# does what it 's supposed to do. A load factor is incorporated
# since cuckoo filters will not fit their theoretical max load.

if __name__ == "__main__":
    # Settings for this test
    max_buckets = 128
    nests_per_bucket = 4
    load_factor = 0.75

    filter = CuckooFilter(max_buckets, nests_per_bucket)

    # setup test variables
    max_items = max_buckets * nests_per_bucket
    num_items_to_test = int(max_items * load_factor)
    fails = 0

    # Add a lot of integers
    for i in range(num_items_to_test):
        i_as_uint8_list = Conversion.uint32_to_uint8_array(i)
        if not filter.add(i_as_uint8_list):
            fails += 1

    print("ADD: ", Status(fails))
    fails = 0

    # check if they ended up in the filter
    for i in range(num_items_to_test):
        i_as_uint8_list = Conversion.uint32_to_uint8_array(i)
        if not filter.contains(i_as_uint8_list):
            fails += 1

    print("CONTAINS: ", Status(fails))
    fails = 0
