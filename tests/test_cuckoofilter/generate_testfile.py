"""
Script for generating a .csv.cuck file with a few parameters.
"""
import sys, os, random

def getPathFromFileName(fname):
    if not fname.find(os.path.pathsep):
        fname = os.path.join(os.path.dirname(__file__), fname)
    return fname


if __name__ == "__main__":
    ### arg parsing
    if len(sys.argv) < 5 + 1:
        print("Usage: python3 generate_testfile.py cuckootestfile 50 4 100 6 20")
        print("arg 0: outputfilename (.csv.cuck will be appended")
        print("arg 1: cuckoo num buckets log 2")
        print("arg 2: cuckoo num items per bucket")
        print("arg 3: number of items to generate")
        print("arg 4: min length of an item")
        print("arg 5: max length of an item")
        quit()

    out_fname  = sys.argv[0 + 1] + ".csv.cuck"
    num_bucks = int(sys.argv[1 + 1])
    num_nests = int(sys.argv[2 + 1])
    num_items = int(sys.argv[3 + 1])
    min_len   = int(sys.argv[4 + 1])
    max_len   = int(sys.argv[5 + 1])
    
    F_out = open(getPathFromFileName(out_fname), "w+")

    print(f"# testparameters num_items:{num_items}, min_len:{min_len}, max_len:{max_len}", file=F_out)
    print(",".join(["cuckoofilter"]+[f"{num_bucks:#0{4}x}",f"{num_nests:#0{4}x}"]), file=F_out)
    for i in range(num_items):
        print(",".join(
                ["add"]+
                [f"{random.getrandbits(8):#0{4}x}" for i in range(random.randint(min_len,max_len))] ), 
            file=F_out)

