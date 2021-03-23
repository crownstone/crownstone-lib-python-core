from crownstone_core.util.cuckoofilter import CuckooFilter

def test_cuckoofilter_api():
    """
    Calls several cuckoo filter functions to ensure they don't run into broken code.
    """
    fingerprintsize = 2
    indexsize = 1
    header_size = fingerprintsize + 2 * indexsize

    bucks = 64
    nests = 4

    num_fingerprints = bucks * nests
    fingerprint_array_size = num_fingerprints * fingerprintsize
    total_size = header_size + fingerprint_array_size

    f = CuckooFilter(bucks, nests)

    assert f.filterhash() <= 0xffff, "filter hash too big"
    assert f.fingerprintcount() == num_fingerprints, "Number of fingerprints in array incorrect"
    assert len(f.bucket_array) == num_fingerprints, "Number of fingerprints in array incorrect"
    assert f.size() == total_size, "Total size of cuckoo filter incorrect"
    assert f.buffersize() == fingerprint_array_size
    assert CuckooFilter.sizeof('CuckooFilter') == header_size

    f.getExtendedFingerprint([1, 2, 3, 4, 5, 6])
    f.add([1, 2, 3, 4, 5, 6])
    assert f.contains([1, 2, 3, 4, 5, 6]), "Contains incorrect after add"
    f.remove([1, 2, 3, 4, 5, 6])
    assert not f.contains([1, 2, 3, 4, 5, 6]), "Contains incorrect after remove"

