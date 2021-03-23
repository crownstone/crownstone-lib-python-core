"""
Generates a <filename>.py.cuck file for a given <filename>.csv.cuck file. Generated file should match
the pregenerated file <filename>.cuck.
Generated .py.cuck files removed after script finishes.
"""
import sys, os, filecmp
from crownstone_core.util.cuckoofilter import CuckooFilter
from crownstone_core.util.Conversion import Conversion


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
            print("Constructing cuckoofilter from file")
            if not columns_len == 3:
                print("invalid amount of arguments for construction of cuckoofilter")
                continue
            if filter is not None:
                print("Ignoring second cuckoofilter definition in file.")
                continue

            buck_count = int(columns[1], 16)
            nest_count = int(columns[2], 16)
            print("construction arguments for cuckoo filter:", buck_count, nest_count)
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

def assertCsv(fname):
    assert fname[-9:] == ".csv.cuck", "file extension should be .csv.cuck"

def process_test_file(in_fname):
    assertCsv(in_fname)

    result_fname = in_fname[:-9] + ".py.cuck"
    expect_fname = in_fname[:-9] + ".cuck"

    cuck_in_path = getPathFromFileName(in_fname)
    cuck_result_path = getPathFromFileName(result_fname)
    cuck_expect_path =  getPathFromFileName(expect_fname)

    filter = None
    with open(cuck_in_path, "r") as F_in:
        filter = loadFilter(F_in)

    if filter is None:
        print("[FAIL] filter couldn't be loaded")
        quit()

    print("writing result file")
    with open(cuck_result_path, "w+") as F_out:
        # header / meta data part:
        write_uint8(F_out, filter.bucket_count)
        write_uint8(F_out, filter.nests_per_bucket)
        write_uint16(F_out, filter.victim.fingerprint)
        write_uint8(F_out, filter.victim.bucketA)
        write_uint8(F_out, filter.victim.bucketB)

        # fingerprint array part:
        for fingerprint in filter.bucket_array:
            write_uint16(F_out, fingerprint)

    # check file equality
    if not filecmp.cmp(cuck_expect_path, cuck_result_path, shallow=False):
        print("[FAIL] Files unequal")
    else:
        print("[OK] Files equal")

    print("cleaning up")
    # delete generated file
    os.remove(cuck_result_path)
    filecmp.clear_cache()


def test_cross_platform_consistency_0():
    process_test_file("./cuckoo_size_128_4_len_6_20.csv.cuck")

