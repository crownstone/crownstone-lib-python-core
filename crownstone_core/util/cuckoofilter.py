from typing import List
from numpy import uint8, uint16, uint32, uint64
from itertools import chain
from crownstone_core.util.CRC import crc16ccitt
from crownstone_core.util.Conversion import Conversion

from crownstone_core.util.randomgenerator import RandomGenerator

class CuckooFilter:
    """
    Cuckoo filter implementation, currently supporting only 16 bit fingerprints.
    """
    max_kick_attempts = int(100)

    # Type aliases, introduced to allow future improvements for other bit-sized fingerprints
    ByteArrayType = List[uint8]
    FingerprintType = uint16
    IndexType = uint8
    FingerprintArrayType = List[FingerprintType]

    class ExtendedFingerprint:
        def __init__(self, fingerprint : 'FingerprintType', bucketA : 'IndexType', bucketB : 'IndexType'):
            self.fingerprint : 'FingerprintType' = fingerprint
            self.bucketA : 'IndexType' = bucketA
            self.bucketB : 'IndexType' = bucketB

        def __str__(self):
            return f"CuckooFilter.ExtendedFingerprint({self.fingerprint:#0{6}x},{self.bucketA:#0{4}x},{self.bucketB:#0{4}x})"

        def __eq__(self, other):
            """ Buckets are allowed to be reversed. Fingerprints must be equal. """
            return self.fingerprint == other.fingerprint and (
                   (self.bucketA == other.bucketA and self.bucketB == other.bucketB) or
                   (self.bucketB == other.bucketA and self.bucketA == other.bucketB)
            )


    def getExtendedFingerprint(self, key : 'ByteArrayType') -> 'ExtendedFingerprint':
        finger = self.hash(key)
        hashed_finger = self.hash(Conversion.uint16_to_uint8_array(finger))

        return CuckooFilter.ExtendedFingerprint(
            finger,
            hashed_finger % self.bucket_count,
            (hashed_finger ^ finger) % self.bucket_count)

    def getExtendedFingerprintFromFingerprintAndBucket(self, fingerprint : 'FingerprintType', bucket_index : 'IndexType'):
        bucket_a = uint8(bucket_index % self.bucket_count)
        bucket_b = uint8((bucket_index ^ fingerprint) % self.bucket_count)
        return CuckooFilter.ExtendedFingerprint (fingerprint, bucket_a, bucket_b)

    # -------------------------------------------------------------
    # Run time variables
    # -------------------------------------------------------------

    def __init__(self, bucket_count : 'IndexType', nests_per_bucket : 'IndexType'):
        self.bucket_count     : 'IndexType'            = bucket_count
        self.nests_per_bucket : 'IndexType'            = nests_per_bucket
        self.victim: 'FingerprintType' = CuckooFilter.ExtendedFingerprint(0,0,0)
        self.bucket_array: 'FingerprintArrayType'

        self.clear()

    # -------------------------------------------------------------
    # ----- Private methods -----
    # -------------------------------------------------------------

    def filterhash(self) -> 'FingerprintType':
        # flatten the uint16 array to uint8 array in little endian. Must match firmware.
        as_uint8_list = list(chain.from_iterable([Conversion.uint16_to_uint8_array(fingerprint) for fingerprint in self.bucket_array]))
        return self.hash(as_uint8_list)

    def getFingerprint(self, key : 'ByteArrayType') -> 'FingerprintType':
        return self.hash(key)

    def hash(self, data : 'ByteArrayType') -> 'FingerprintType':
        return uint16(crc16ccitt(data))

    def scramble(self, fingerprint : 'FingerprintType') -> 'FingerprintType':
        """
         this implementation hinges on the fact that 2**16+1 is prime,
         and that n-> n^17 is a bijection mod 2**16 + 1.
        :param fingerprint:
        :return:
        """
        x = int(uint16(fingerprint)) # native python int does't overflow, but input needs to be truncated.

        if x == 0:
            # lift 0 to 2**16 to get rid of silly problems involving 0.
            x = 0x10000

        y = (x * x) % 0x10001  # y == x^2  mod (2**16+1)
        y = (y * y) % 0x10001  # y == x^4  mod (2**16+1)
        y = (y * y) % 0x10001  # y == x^8  mod (2**16+1)
        y = (y * y) % 0x10001  # y == x^16 mod (2**16+1)
        y = (y * x) % 0x10001  # y == x^17 mod (2**16+1)

        return uint16(y) # intentional truncation to 16 bits (0x10000 -> 0)

    def lookup_fingerprint(self, bucket_number : 'IndexType', finger_index : 'IndexType') -> 'FingerprintType':
        return self.bucket_array[self.lookup_fingerprint_index(bucket_number, finger_index)]

    def lookup_fingerprint_index(self, bucket_number : 'IndexType', finger_index : 'IndexType') -> 'FingerprintType':
         return (bucket_number * self.nests_per_bucket) + finger_index

    def add_fingerprint_to_bucket (self, fingerprint : 'FingerprintType', bucket_number : 'IndexType') -> bool:
        for ii in range(self.nests_per_bucket):
            fingerprint_index = self.lookup_fingerprint_index(bucket_number, ii)
            if 0 == self.bucket_array[fingerprint_index]:
                self.bucket_array[fingerprint_index] = fingerprint
                return True
        return False

    def remove_fingerprint_from_bucket (self, fingerprint : 'FingerprintType', bucket_number : 'IndexType') -> bool :
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
    def moveExtendedFingerprint(self, entry_to_insert : 'ExtendedFingerprint') -> bool:
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

    def addExtendedFingerprint(self, efp : 'ExtendedFingerprint') -> bool:
        if self.containsExtendedFingerprint(efp):
            return True

        if self.victim.fingerprint != 0: # already full.
            return False

        return self.moveExtendedFingerprint(efp)

    def removeExtendedFingerprint(self, efp : 'ExtendedFingerprint') -> bool:
        if self.remove_fingerprint_from_bucket(efp.fingerprint, efp.bucketA) or \
                self.remove_fingerprint_from_bucket(efp.fingerprint, efp.bucketB):
            # short ciruits nicely:
            #    tries bucketA,
            #    on fail try B,
            #    if either succes, fix victim.
            if self.victim.fingerprint !=  0:
                if self.addExtendedFingerprint(self.victim):
                    self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
            return True
        return False

    def containsExtendedFingerprint(self, efp : 'ExtendedFingerprint') -> bool:
        # (loops are split to improve cache hit rate)
        # search bucketA
        for ii in range(self.nests_per_bucket):
            if efp.fingerprint == self.lookup_fingerprint(efp.bucketA, ii):
                return True
        # search bucketA
        for ii in range(self.nests_per_bucket):
            if efp.fingerprint == self.lookup_fingerprint(efp.bucketB, ii):
                return True

        return False

    # -------------------------------------------------------------

    def addFingerprintType(self, fp : 'FingerprintType', bucket_index : 'IndexType') -> bool:
        return self.addExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fp, bucket_index))


    def removeFingerprintType(self, fp : 'FingerprintType', bucket_index : 'IndexType') -> bool:
        return self.removeExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fp, bucket_index))


    def containsFingerprintType(self, fp : 'FingerprintType', bucket_index : 'IndexType') -> bool:
        return self.containsExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fp, bucket_index))

    # -------------------------------------------------------------

    def add(self, key : 'ByteArrayType') -> bool:
        return self.addExtendedFingerprint(self.getExtendedFingerprint(key))

    def remove(self, key : 'ByteArrayType') -> bool:
        return self.removeExtendedFingerprint(self.getExtendedFingerprint(key))

    def contains(self, key : 'ByteArrayType') -> bool:
        return self.containsExtendedFingerprint(self.getExtendedFingerprint(key))


    # -------------------------------------------------------------
    # Init/deinit like stuff.
    # -------------------------------------------------------------

    def clear(self):
        self.victim: 'FingerprintType' = CuckooFilter.ExtendedFingerprint(0,0,0)
        self.bucket_array: 'FingerprintArrayType' = [uint16(0)] * CuckooFilter.getfingerprintcount(self.bucket_count,
                                                                                                   self.nests_per_bucket)

    # -------------------------------------------------------------
    # Size stuff.
    # -------------------------------------------------------------

    @staticmethod
    def sizeof(typ) -> uint32:
        D = {
            'uint8': 1,
            'uint16': 2,
            'uint32': 4,
            'uint64': 8,
            'CuckooFilter': 1 + 1 + 2,
            'FingerprintType': 2,
        }
        if typ in D:
            return D[typ]
        return -1

    @staticmethod
    def getfingerprintcount(bucket_count : 'IndexType', nests_per_bucket : 'IndexType') -> uint32:
        return uint32(bucket_count * nests_per_bucket)

    @staticmethod
    def getbuffersize(bucket_count: 'IndexType', nests_per_bucket: 'IndexType') -> uint32:
        return CuckooFilter.getfingerprintcount(bucket_count, nests_per_bucket) * CuckooFilter.sizeof('FingerprintType')

    @staticmethod
    def getsize(bucket_count: 'IndexType', nests_per_bucket: 'IndexType') -> uint32:
        return CuckooFilter.sizeof(CuckooFilter) + CuckooFilter.getbuffersize(bucket_count, nests_per_bucket)

    def fingerprintcount(self) -> uint32:
        return CuckooFilter.getfingerprintcount(self.bucket_count, self.nests_per_bucket)

    def buffersize(self) -> uint32:
        return CuckooFilter.getbuffersize(self.bucket_count, self.nests_per_bucket)

    def size(self) -> uint32:
        return CuckooFilter.getsize(self.bucket_count, self.nests_per_bucket)


if __name__ == "__main__":
    f = CuckooFilter(50, 4)

    print("filter hash: " + hex(f.filterhash()))
    print("fingerprint array len: " + str(len(f.bucket_array)) )
    print("size: " + str(f.size()))
    print("buffersize: " + str(f.buffersize()))
    print("fingerprints: " + str(f.fingerprintcount()))
    print("sizeof overhead: " + str(CuckooFilter.sizeof('CuckooFilter')))
    f.getExtendedFingerprint([1, 2, 3, 4, 5, 6])
    f.add([1, 2, 3, 4, 5, 6])
    print("[OK] contained!" if f.contains([1, 2, 3, 4, 5, 6]) else "[FAIL] not contained!")
    f.remove([1, 2, 3, 4, 5, 6])
    print("[FAIL] contained!" if f.contains([1, 2, 3, 4, 5, 6]) else "[OK] not contained!")
    print("end")
