import os
import sys
import re
import glob
from tqdm import tqdm
import pandas as pd

if __name__ == "__main__":
    from util import *
else:
    from .util import *

# check argument
assert len(sys.argv) == 2, \
    "Invalid arguments. Only one file or directory is allowed."

# python file path
abs_dir = os.path.dirname(__file__)
name = sys.argv[1]


def parse_gff(filename):
    # parse the gff file
    line = []
    try:
        with open(filename, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith("##FASTA"):
                    break
                if read_line.startswith(("##", "#!")) or read_line == "":
                    continue
                line.append(read_line)
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")
        return

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
            "gene": [],
            "product": []}

    for i, column in enumerate(line):
        value = column.split("\t")
        try:
            # for NCBI gff3 screening
            if value[2] == "gene":
                continue

            value_list = [value[item] for item in (0, 3, 4)]
            attr_ec = re.search("eC_number=([^;]*)", value[8])
            attr_gene = re.search("gene=([^;]*)", value[8])
            attr_product = re.search("product=([^;]*)", value[8])
            for attr in (attr_ec, attr_gene, attr_product): 
                if attr is not None:
                    attr = attr.group(1).strip("\n")
                    value_list.append(attr)
                else:
                    value_list.append("-")
            for num, key in enumerate(data):
                data[key].append(value_list[num])
        except IndexError:
            print(f"index error at line: {i}")
            repr(column)

    data = pd.DataFrame(data)
    return data


if os.path.isdir(name):
    # find gff files in the directory
    file_list = glob.glob(os.path.join(name, "**/*.gff"), recursive=True)
    file_list.extend(glob.glob(os.path.join(name, "**/*.gff3"), recursive=True))
    file_list = [file.replace("\\", "/") for file in file_list]
    for filename in tqdm(file_list):
        data = parse_gff(filename)
        # use the folder name as the final filename
        data.to_csv(create_savename(abs_dir, filename.split("/")[-2]),
                    index=False)
elif os.path.isfile(name):
    data = parse_gff(name)
    data.to_csv(create_savename(abs_dir, name))
else:
    print("Invalid file or directory name")
    sys.exit()
