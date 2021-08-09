"""
Generates a <filename>.py.cuck file for a given <filename>.csv.cuck file. Generated file should match
the pregenerated file <filename>.cuck.
Generated .py.cuck files removed after script finishes.
"""
import os, filecmp
from crownstone_core.util.Cuckoofilter import CuckooFilter
from crownstone_core.util.Conversion import Conversion


def loadFilter(infile):
    """
    Takes a file object and creates a CuckooFilter constructed from its contents.
    """
    filter = None
    fails = 0
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
            if not filter.add([ int(x, 16) for x in columns[1:] ]):
                fails += 1
        else:
            # operation not recognized, ignore
            continue

    assert fails == 0
    return filter

def write_uint8(outfile, val):
    outfile.write(f"{val:#0{4}x},")

def write_uint16(outfile, val):
    for byt in Conversion.uint16_to_uint8_array(val):
        write_uint8(outfile, byt)

# ------------------------------------------------------------

def getPathFromFileName(fname):
    if not os.path.isabs(fname):
        return os.path.join(os.path.dirname(__file__), fname)
    return fname

def assertCsv(fname):
    assert fname[-9:] == ".csv.cuck", "file extension should be .csv.cuck"

def get_input_file_path(csv_cuck_file):
    return getPathFromFileName(csv_cuck_file)

def get_result_file_path(csv_cuck_file):
    result_fname = csv_cuck_file[:-9] + ".py.cuck"
    return getPathFromFileName(result_fname)

def get_expect_file_path(csv_cuck_file):
    expect_fname = csv_cuck_file[:-9] + ".cuck"
    return getPathFromFileName(expect_fname)

# ------------------------------------------------------------

def read_filter(csv_cuck_file_path):
    filter = None
    with open(csv_cuck_file_path, "r") as F_in:
        filter = loadFilter(F_in)
    return filter

def write_filter(filter, output_path):
    # writing result file
    with open(output_path, "w+") as F_out:
        for byt in filter.serialize():
            write_uint8(F_out, byt)

# ------------------------------------------------------------

def process_test_file(csv_cuck_file):
    assertCsv(csv_cuck_file)

    cuck_input_path = getPathFromFileName(csv_cuck_file)
    cuck_result_path = get_result_file_path(csv_cuck_file)
    cuck_expect_path = get_expect_file_path(csv_cuck_file)

    filter = read_filter(cuck_input_path)

    assert filter is not None,"filter couldn't be loaded"

    write_filter(filter, cuck_result_path)

    # check file equality
    assert filecmp.cmp(cuck_expect_path, cuck_result_path, shallow=False), "Generated test file unequal precomputed file"

    # delete generated file
    os.remove(cuck_result_path)
    filecmp.clear_cache()


# ------------------------------------------------------------
# ------------------------------------------------------------

def test_cross_platform_consistency_0():
    process_test_file("./cuckoo_size_128_4_len_6_20.csv.cuck")


if __name__ == "__main__":
    """
    If this script is run as stand alone, it will regenerate the .cuck file(s) based on the current
    implementation of the cuckoo filter. Only run this is you are 100% absolutely mega certain that
    the implementation is correct. 
    """
    files_to_generate = []
    files_to_generate += ["./cuckoo_size_128_4_len_6_20.csv.cuck"]

    if not files_to_generate:
        print("files might be commented out for safety")

    for csv_cuck_file in files_to_generate:
        print("Regenerating test file ", csv_cuck_file)
        assertCsv(csv_cuck_file)
        cuck_input_path = getPathFromFileName(csv_cuck_file)
        filter = read_filter(cuck_input_path)
        if filter is None:
            print("Filter failed to construct. Be careful when generating expectation definition files!")
            quit()
        write_filter(filter,get_expect_file_path(csv_cuck_file))


