from itertools import chain
from crownstone_core.util.CRC import crc16ccitt
from crownstone_core.util.Conversion import Conversion

from crownstone_core.util.randomgenerator import RandomGenerator

class CuckooFilter:
    """
    Cuckoo filter implementation, currently supporting only 16 bit fingerprints.

    Expected types for arguments and return values:
    - ByteArrayType = List[uint8]
    - FingerprintType = uint16
    - IndexType = uint8
    - FingerprintArrayType = List[FingerprintType]
    """
    max_kick_attempts = int(100)

    class ExtendedFingerprint:
        def __init__(self, fingerprint, bucketA, bucketB):
            self.fingerprint = fingerprint
            self.bucketA = bucketA
            self.bucketB = bucketB

        def __str__(self):
            return f"CuckooFilter.ExtendedFingerprint({self.fingerprint:#0{6}x},{self.bucketA:#0{4}x},{self.bucketB:#0{4}x})"

        def __eq__(self, other):
            """ Buckets are allowed to be reversed. Fingerprints must be equal. """
            return self.fingerprint == other.fingerprint and (
                   (self.bucketA == other.bucketA and self.bucketB == other.bucketB) or
                   (self.bucketB == other.bucketA and self.bucketA == other.bucketB)
            )

    def getExtendedFingerprint(self, key):
        """
        key: FingerprintType
        returns ExtendedFingerprint
        """
        finger = self.hash(key)
        hashed_finger = self.hash(Conversion.uint16_to_uint8_array(finger))

        return CuckooFilter.ExtendedFingerprint(
            finger,
            hashed_finger % self.bucket_count,
            (hashed_finger ^ finger) % self.bucket_count)

    def getExtendedFingerprintFromFingerprintAndBucket(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        bucket_index: IndexType
        returns: ExtendedFingerprint
        """
        bucket_a = (bucket_index % self.bucket_count) & 0xff
        bucket_b =((bucket_index ^ fingerprint) % self.bucket_count) & 0xff
        return CuckooFilter.ExtendedFingerprint (fingerprint, bucket_a, bucket_b)

    # -------------------------------------------------------------
    # Run time variables
    # -------------------------------------------------------------

    def __init__(self, bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: n/a
        """
        self.bucket_count = bucket_count
        self.nests_per_bucket = nests_per_bucket
        self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
        self.bucket_array = []

        self.clear()

    # -------------------------------------------------------------
    # ----- Private methods -----
    # -------------------------------------------------------------

    def filterhash(self):
        """
        Flatten the uint16 array of fingerprints to uint8 array in little endian. Must match firmware.

        returns: FingerprintType
        """
        as_uint8_list = list(chain.from_iterable(
            [Conversion.uint16_to_uint8_array(fingerprint) for fingerprint in self.bucket_array]
        ))
        return self.hash(as_uint8_list)

    def getFingerprint(self, key):
        """
        key: IndexType
        returns: FingerprintType
        """
        return self.hash(key)

    def hash(self, data):
        """
        data: ByteArraytype
        returns: FingerprintType
        """
        return crc16ccitt(data)

    def lookup_fingerprint(self, bucket_number, finger_index):
        """
        bucket_number: IndexType
        finger_index: IndexType
        returns: FingerprintType
        """
        return self.bucket_array[self.lookup_fingerprint_index(bucket_number, finger_index)]

    def lookup_fingerprint_index(self, bucket_number, finger_index):
        """
        bucket_number: IndexType
        finger_index: IndexType
        returns: int
        """
        return (bucket_number * self.nests_per_bucket) + finger_index

    def add_fingerprint_to_bucket (self, fingerprint, bucket_number):
        """
        fignerprint: FingerprintType
        bucket_number: IndexType
        returns: bool
        """
        for ii in range(self.nests_per_bucket):
            fingerprint_index = self.lookup_fingerprint_index(bucket_number, ii)
            if 0 == self.bucket_array[fingerprint_index]:
                self.bucket_array[fingerprint_index] = fingerprint
                return True
        return False

    def remove_fingerprint_from_bucket (self, fingerprint, bucket_number):
        """
        fignerprint: FingerprintType
        bucket_number: IndexType
        returns: bool
        """
        for ii in range(self.nests_per_bucket):
            candidate = self.lookup_fingerprint_index(bucket_number, ii) # candidate_fingerprint_for_removal_in_array_index

            if self.bucket_array[candidate] == fingerprint:
                self.bucket_array[candidate] = 0
                # to keep the bucket front loaded, move the last non-zero
                # fingerprint behind ii into the slot.
                for jj in reversed(range(ii + 1, self.nests_per_bucket)):
                    last = self.lookup_fingerprint_index(bucket_number, jj) # last_fingerprint_in_bucket

                    if self.bucket_array[last] != 0:
                        self.bucket_array[candidate] = self.bucket_array[last]
                return True
        return False

    # -------------------------------------------------------------
    def moveExtendedFingerprint(self, entry_to_insert):
        """
        entry_to_insert: ExtendedFingerprint
        returns: bool
        """
        # seeding with a hash for this filter guarantees exact same sequence of
        # random integers used for moving fingerprints in the filter on every crownstone.
        seed = self.filterhash()
        rand = RandomGenerator(seed)

        for attempts_left in range(CuckooFilter.max_kick_attempts):
            # try to add to bucket A
            if self.add_fingerprint_to_bucket(entry_to_insert.fingerprint, entry_to_insert.bucketA):
                return True

            # try to add to bucket B
            if self.add_fingerprint_to_bucket(entry_to_insert.fingerprint, entry_to_insert.bucketB):
                return True

            # no success, time to kick a fingerprint from one of our buckets

            # determine which bucket to kick from
            kick_A = rand() % 2
            kicked_item_bucket =  entry_to_insert.bucketA if kick_A else entry_to_insert.bucketB

            # and which fingerprint index
            kicked_item_index = rand() % self.nests_per_bucket

            # swap entry to insert and the randomly chosen ('kicked') item
            kicked_item_fingerprint_index = self.lookup_fingerprint_index(kicked_item_bucket, kicked_item_index)
            kicked_item_fingerprint_value = self.bucket_array[kicked_item_fingerprint_index]

            self.bucket_array[kicked_item_fingerprint_index] = entry_to_insert.fingerprint

            entry_to_insert = self.getExtendedFingerprintFromFingerprintAndBucket(
                kicked_item_fingerprint_value, kicked_item_bucket)

            # next iteration will try to re-insert the footprint previously at (h,i).

        # iteration ended: failed to re-place the last kicked entry into the buffer after max attempts.
        self.victim = entry_to_insert

        return False

    def addExtendedFingerprint(self, extended_finger):
        """
        extended_finger: ExtendedFingerprint
        returns: bool
        """
        if self.containsExtendedFingerprint(extended_finger):
            return True

        if self.victim.fingerprint != 0: # already full.
            return False

        return self.moveExtendedFingerprint(extended_finger)

    def removeExtendedFingerprint(self, extended_finger):
        """
        extended_finger: ExtendedFingerprint
        returns: bool
        """
        if self.remove_fingerprint_from_bucket(extended_finger.fingerprint, extended_finger.bucketA) or \
                self.remove_fingerprint_from_bucket(extended_finger.fingerprint, extended_finger.bucketB):
            # short ciruits nicely:
            #    tries bucketA,
            #    on fail try B,
            #    if either succes, fix victim.
            if self.victim.fingerprint !=  0:
                if self.addExtendedFingerprint(self.victim):
                    self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
            return True
        return False

    def containsExtendedFingerprint(self, extended_finger):
        """
        extended_finger: ExtendedFingerprint
        returns: bool
        """
        # (loops are split to improve cache hit rate)
        # search bucketA
        for ii in range(self.nests_per_bucket):
            if extended_finger.fingerprint == self.lookup_fingerprint(extended_finger.bucketA, ii):
                return True
        # search bucketA
        for ii in range(self.nests_per_bucket):
            if extended_finger.fingerprint == self.lookup_fingerprint(extended_finger.bucketB, ii):
                return True

        return False

    # -------------------------------------------------------------

    def addFingerprintType(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        returns: bool
        """
        return self.addExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fingerprint, bucket_index))


    def removeFingerprintType(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        bucket_index: Indextype
        returns: bool
        """
        return self.removeExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fingerprint, bucket_index))


    def containsFingerprintType(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        bucket_index: IndexType
        returns: bool
        """
        return self.containsExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fingerprint, bucket_index))

    # -------------------------------------------------------------

    def add(self, key):
        """
        key: ByteArrayType
        returns: bool
        """
        return self.addExtendedFingerprint(self.getExtendedFingerprint(key))

    def remove(self, key):
        """
        key: ByteArrayType
        returns: bool
        """
        return self.removeExtendedFingerprint(self.getExtendedFingerprint(key))

    def contains(self, key):
        """
        key: ByteArrayType
        returns: bool
        """
        return self.containsExtendedFingerprint(self.getExtendedFingerprint(key))


    # -------------------------------------------------------------
    # Init/deinit like stuff.
    # -------------------------------------------------------------

    def clear(self):
        """
        returns: None
        """
        self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
        self.bucket_array = [0x00] * CuckooFilter.getfingerprintcount(self.bucket_count, self.nests_per_bucket)

    # -------------------------------------------------------------
    # Size stuff.
    # -------------------------------------------------------------

    @staticmethod
    def sizeof(typ):
        size_dict = {
            'uint8': 1,
            'uint16': 2,
            'uint32': 4,
            'uint64': 8,
            'CuckooFilter': 1 + 1 + 2,
            'FingerprintType': 2,
            'IndexType': 1
        }
        if typ in size_dict:
            return size_dict[typ]
        return -1

    @staticmethod
    def getfingerprintcount(bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: int
        """
        return bucket_count * nests_per_bucket

    @staticmethod
    def getbuffersize(bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: int
        """
        return CuckooFilter.getfingerprintcount(bucket_count, nests_per_bucket) * CuckooFilter.sizeof('FingerprintType')

    @staticmethod
    def getsize(bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: int
        """
        return CuckooFilter.sizeof('CuckooFilter') + CuckooFilter.getbuffersize(bucket_count, nests_per_bucket)

    def fingerprintcount(self):
        """
        returns: int
        """
        return CuckooFilter.getfingerprintcount(self.bucket_count, self.nests_per_bucket)

    def buffersize(self):
        """
        returns: int
        """
        return CuckooFilter.getbuffersize(self.bucket_count, self.nests_per_bucket)

    def size(self):
        """
        returns: int
        """
        return CuckooFilter.getsize(self.bucket_count, self.nests_per_bucket)


