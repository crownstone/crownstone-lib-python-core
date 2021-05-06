from crownstone_core.util.Cuckoofilter import CuckooFilter

def Status(fails):
    if fails > 0:
        return "{0}[FAIL]{1} ({2})".format("*", "*", fails)
    else:
        return "[OK]"

    

def test_add_contains_remove_contains():
    """
    Checks if the sequence _contains, _add, _contains, _remove, contains does what it is expected to do.
    """
    # Settings for this test
    max_buckets_log2 = 7
    nests_per_bucket = 4
    load_factor = 0.75

    filter = CuckooFilter(max_buckets_log2, nests_per_bucket)

    # setup test variables
    fails = 0

    # check if it contains "test"
    if filter.contains("test".encode("utf-8")):
        fails += 1
    
    assert fails == 0, "Contains incorrect on empty filter"
    fails = 0

    # add "test"
    if filter.add("test".encode("utf-8")) == False:
        fails += 1
    
    assert fails == 0, "Add fails on empty filter"
    fails = 0

    # check if it contains "test"
    if filter.contains("test".encode("utf-8")) == False:
        fails += 1
    
    assert fails == 0, "Contains incorrect immediately after adding"
    fails = 0

    # remove "test"
    if filter.remove("test".encode("utf-8")) == False:
        fails += 1
    
    assert fails == 0, "Remove fails"
    fails = 0

    # check if it contains "test"
    if filter.contains("test".encode("utf-8")):
        fails += 1
    
    assert fails == 0, "Contains incorrect immediately after removal"
    fails = 0

