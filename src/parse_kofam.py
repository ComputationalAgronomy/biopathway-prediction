import os
import sys
import re
import pandas as pd

if __name__ == "__main__":
    from util import *
else:
    from .util import *
 
# check argument
assert len(sys.argv) == 3, "Invalid arguments."

# python file path
abs_dir = os.path.dirname(__file__)
file1 = sys.argv[1] # orignal protein fasta
file2 = sys.argv[2]

try:
    line_1 = []
    with open(file1, "r") as f:
        for read_line in f.readlines():
            if read_line.startswith(">"):
                line_1.append([read_line])
                line_1[-1].append("")
            else:
                try:
                    # keep protein fasta sequence in case
                    # we want to use it later
                    line_1[-1][1] += read_line.strip("\n")
                except IndexError:
                    print("Error in input format")
                    sys.exit()
except FileNotFoundError:
    print(f"Cannot find the file1")
    sys.exit()

try:
    line_2 = []
    with open(file2, "r") as f:
        for read_line in f.readlines():
            if read_line.startswith("*"):
                line_2.append(read_line)
except FileNotFoundError:
    print(f"Cannot find the file2")
    sys.exit()

# parse files

data_1 = {"sequence_no": [],
          "start": [],
          "end": []
         }

# extract columns
# kofamscan
# column
# 0: *
# 1: sequence no
# 2: KO id
# 3: threshold 
# 4: score
# 5: e_value
# 6: KO definition

data_2 = {"sequence_no": [],
        "KO": [],
        "ec_number": [],
        "product": []}

for i, content in enumerate([x[0] for x in line_1]):
    columns = content.split(maxsplit=1)
    value_list = []
    seq = re.search("_(\d+)$", columns[0])
    start = re.search("location=[a-z]*\(?(\d+)", columns[1])
    end = re.search("location=[a-z]*\(?\d+\.\.(\d+)", columns[1])
    for attr in (seq, start, end): 
        if attr is not None:
            attr = attr.group(1)
            value_list.append(attr)
        else:
            value_list.append("-")
    for num, key in enumerate(data_1):
        data_1[key].append(value_list[num])

for i, content in enumerate(line_2):
    columns = content.split(maxsplit=6)
    value_list = []
    seq = re.search("_(\d+)$", columns[1])
    ko = columns[2]
    ec = re.search("EC:([^\]]+)", columns[6])
    product = re.search("([^\[]*)", columns[6])
    for attr in (seq, ko, ec, product): 
        if attr is not None:
            if not isinstance(attr, str):
                attr = attr.group(1).strip(" ").strip("\n").strip("\"")
            value_list.append(attr)
        else:
            value_list.append("-")
    for num, key in enumerate(data_2):
        data_2[key].append(value_list[num])

data_1 = pd.DataFrame(data_1)
data_2 = pd.DataFrame(data_2)

data_1.to_csv(create_savename(abs_dir, file1), index=False)
data_2.to_csv(create_savename(abs_dir, file2), index=False)

