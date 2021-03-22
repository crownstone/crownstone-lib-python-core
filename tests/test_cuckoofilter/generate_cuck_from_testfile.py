import sys, os
from py.cuckoofilter import CuckooFilter
from crownstone_core.util.Conversion import Conversion

def assertCsv(fname):
    if not fname[-4:] == ".csv":
        print(F"file should be .csv, got {fname}")
        quit()

def getPathFromFileName(fname):
    if not fname.find(os.path.pathsep):
        fname = os.path.join(os.path.dirname(__file__), fname)
    return fname


def loadFilter(infile):
    filter = None

    for line in infile:
        # strip trailing comments:
        line = line.strip()
        comment_token_index = line.find("#")
        if comment_token_index >= 0:
            line = line[ : comment_token_index]

        if len(line) == 0:
            # ignore (resulting) empty lines
            continue

        columns = line.split(",")
        columns_len = len(columns)
        operation = columns[0]

        if operation == "cuckoofilter":
            print("processing operation cuckoofilter")
            if not columns_len == 3:
                print("invalid amount of arguments for construction of cuckoofilter")
                continue
            if filter is not None:
                print("Ignoring second cuckoofilter definition in file.")
                continue

            buck_count = int(columns[1], 16)
            nest_count = int(columns[2], 16)
            print("constructing arguments for cuckoo filter:", buck_count, nest_count)
            filter = CuckooFilter(buck_count, nest_count)
        elif operation == "add":
            if filter is None:
                print("skipping add command, filter not yet constructed")
                continue
            filter.add([ int(x, 16) for x in columns[1:] ])
        else:
            print("operation not recognized: ")
            continue

    return filter


def write_uint8(outfile, val):
    outfile.write(f"{val:#0{4}x},")

def write_uint16(outfile, val):
    for byt in Conversion.uint16_to_uint8_array(val):
        write_uint8(outfile, byt)


if __name__ == "__main__":
    """
    Generates a <filename>.py.cuck file for a given <filename>.csv file. Generated file should match 
    the pregenerated file <filename>.cuck. 
    """
    ### arg parsing
    if len(sys.argv) < 1 + 1:
        print("Usage: python3 generate_testfile.py cuckootestfile.csv len({0})".format(len(sys.argv)))
        print(sys.argv)
        print("arg 0: input filename relative to this script (e.g. ./testdb.csv)")
        quit()

    in_fname = sys.argv[0 + 1]

    assertCsv(in_fname)

    out_fname = in_fname[:-4] + ".py.cuck"
    print(getPathFromFileName(out_fname))
    print(getPathFromFileName(in_fname))

    filter = None
    with open(getPathFromFileName(in_fname), "r") as F_in:
        filter = loadFilter(F_in)

    if filter is None:
        print("failed to load filter")
        quit()

    with open(getPathFromFileName(out_fname), "w+") as F_out:
        # header / meta data part:
        write_uint8(F_out, filter.bucket_count)
        write_uint8(F_out, filter.nests_per_bucket)
        write_uint16(F_out, filter.victim.fingerprint)
        write_uint8(F_out, filter.victim.bucketA)
        write_uint8(F_out, filter.victim.bucketB)

        # fingerprint array part:
        for fingerprint in filter.bucket_array:
            write_uint16(F_out, fingerprint)
