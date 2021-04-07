"""
Generates a <filename>.py.cuck file for a given <filename>.csv.cuck file. Generated file should match
the pregenerated file <filename>.cuck.
Generated .py.cuck files removed after script finishes.
"""
import sys, os, filecmp
from crownstone_core.util.cuckoofilter import CuckooFilter
from crownstone_core.util.Conversion import Conversion


def getPathFromFileName(fname):
    if not os.path.isabs(fname):
        return os.path.join(os.path.dirname(__file__), fname)
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
            # Constructing cuckoofilter from file
            assert columns_len == 3, "Testfile corrput: invalid amount of arguments for construction of cuckoofilter"
            assert filter is None, "Testfile corrupt: second cuckoofilter definition in file."

            buck_count = int(columns[1], 16)
            nest_count = int(columns[2], 16)
            filter = CuckooFilter(buck_count, nest_count)
        elif operation == "add":
            assert filter is not None, "Testfile corrupt: add command found before filter is constructed"
            filter.add([ int(x, 16) for x in columns[1:] ])
        else:
            # operation not recognized, ignore
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

    assert filter is not None,"filter couldn't be loaded"

    # writing result file
    with open(cuck_result_path, "w+") as F_out:
        for byt in filter.getPacket():
            write_uint8(F_out, byt)

    # check file equality
    assert filecmp.cmp(cuck_expect_path, cuck_result_path, shallow=False), "Generated test file unequal precomputed file"

    # delete generated file
    os.remove(cuck_result_path)
    filecmp.clear_cache()


def test_cross_platform_consistency_0():
    process_test_file("./cuckoo_size_128_4_len_6_20.csv.cuck")

