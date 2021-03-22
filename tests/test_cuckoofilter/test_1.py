from crownstone_core.util.cuckoofilter import CuckooFilter

def Status(fails):
    if fails > 0:
        return "{0}[FAIL]{1} ({2})".format("*", "*", fails)
    else:
        return "[OK]"

    
"""
Checks if the sequence _new, _contains, _add, _contains, _remove, contains, _free does what it is expected to do.
"""
if __name__ == "__main__":
    # Settings for this test
    max_buckets = 128
    nests_per_bucket = 4
    load_factor = 0.75

    filter = CuckooFilter(max_buckets, nests_per_bucket)

    # setup test variables
    fails = 0

    # check if it contains "test"
    if filter.contains("test".encode("utf-8")):
        fails += 1
    
    print("CONTAINS 0" , Status(fails) )
    fails = 0

    # add "test"
    if filter.add("test".encode("utf-8")) == False:
        fails += 1
    
    print("ADD 0" , Status(fails) )
    fails = 0

    # check if it contains "test"
    if filter.contains("test".encode("utf-8")) == False:
        fails += 1
    
    print("CONTAINS 1" , Status(fails) )
    fails = 0

    # remove "test"
    if filter.remove("test".encode("utf-8")) == False:
        fails += 1
    
    print("REMOVE" , Status(fails) )
    fails = 0

    # check if it contains "test"
    if filter.contains("test".encode("utf-8")):
        fails += 1
    
    print("CONTAINS 2" , Status(fails) )
    fails = 0

