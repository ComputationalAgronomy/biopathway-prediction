import os
import sys
import re
import pandas as pd

if __name__ == "__main__":
    from util import *
else:
    from .util import *

# check argument
assert len(sys.argv) == 2, \
    "Invalid arguments. Your current input is: " + sys.argv

# python file path
abs_dir = os.path.dirname(__file__)
filename = sys.argv[1]

# parse the gff file
line = []
try:
    with open(filename, "r") as f:
        for read_line in f.readlines():
            if read_line.startswith("##FASTA"):
                break
            if read_line.startswith("##"):
                continue
            line.append(read_line)
except FileNotFoundError:
    print(f"Cannot find '{filename}'")
    sys.exit()

# extract columns
# column
# 1: sequence ID
# 2: source
# 3: feature type (mRNA, domain, exon, ...)
# 4: feature start
# 5: feature end
# 6: score (e_value or p_value for predictions)
# 7: strand
# 8: phase
# 9: attributes

# 1, 4, 5, 9
data = {"ID": [],
        "start": [],
        "end": [],
        "ec_number": [],
        "product": []}

for i, column in enumerate(line):
    value = column.split("\t")
    try:
        # for NCBI gff3 screening
        if value[2] == "gene":
            continue

        value_list = [value[item] for item in (0, 3, 4)]
        attr_ec = re.search("eC_number=([^;]*)", value[8])
        attr_product = re.search("product=([^;]*)", value[8])
        if attr_ec is not None:
            attr_ec = attr_ec.group(1)
            value_list.append(attr_ec)
        else:
            value_list.append("-")
        if attr_product is not None:
            attr_product = attr_product.group(1).strip("\n")
            value_list.append(attr_product)
        else:
            value_list.append("-")

        for num, key in enumerate(data):
            data[key].append(value_list[num])
    except IndexError:
        print(f"index error at line: {i}")
        print(f"{column}")

data = pd.DataFrame(data)
data.to_csv(create_savename(abs_dir, filename), index=False)
