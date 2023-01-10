import os
import sys
import glob
from tqdm import tqdm

import numpy as np

from src.pathway import pathway_list, enzyme_list


compound_dict = {}
compound_name = {}
enzyme_dict = {}
enzyme_name = {}

def parse_result(filename):
    compound_id = 0
    enzyme_id = 0
    count_compound, count_enzyme = False, False
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip("\n")
            if line == "Compound list:":
                count_compound, count_enzyme = True, False
                continue
            elif line == "Enzyme list:":
                count_compound, count_enzyme = False, True
                continue
            elif line == "":
                continue
            else:
                if count_compound:
                    compound_id += 1
                    exist = eval(line.split(":")[1])
                    try:
                        compound_dict[compound_id] += exist
                    except KeyError:
                        compound_dict[compound_id] = exist
                elif count_enzyme:
                    enzyme_id += 1
                    num = float(line.split(":")[1])
                    try:
                        enzyme_dict[enzyme_id] += num
                    except KeyError:
                        enzyme_dict[enzyme_id] = num


def get_name(filename):
    compound_id = 0
    enzyme_id = 0
    with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip("\n")
                if line == "Compound list:":
                    count_compound, count_enzyme = True, False
                    continue
                elif line == "Enzyme list:":
                    count_compound, count_enzyme = False, True 
                    continue
                elif line == "":
                    continue
                else:
                    if count_compound:
                        compound_id += 1
                        name = line.split(":")[0]
                        compound_name[compound_id] = f"{compound_id}_{name}"
                    elif count_enzyme:
                        enzyme_id += 1
                        name = line.split(":")[0]
                        enzyme_name[enzyme_id] = f"{enzyme_id}_{name}"


def cytoscape_format_conversion(path, output_path):
    if os.path.isdir(path):
        # find gff files in the directory
        file_list = glob.glob(os.path.join(path, "**/*.txt"), recursive=True)
        file_list = [file.replace("\\", "/") for file in file_list]
        get_name(file_list[0])
        for filename in tqdm(file_list):
            parse_result(filename)
        with open(os.path.join(output_path, "network_edge.csv"), "w") as f:
            f.writelines("Reactant,Product,Enzyme,Enzyme_score\n")
            for key, node in pathway_list.items():
                for enzyme_num in node.next_enzyme:
                    enzyme = enzyme_list[enzyme_num]
                    try:
                        f.writelines(f"{compound_name[key]},{compound_name[enzyme.product]},{enzyme.name},{enzyme_dict[enzyme_num]}\n")
                    except AttributeError:
                        pass
        with open(os.path.join(output_path, "network_node.csv"), "w") as f:
            f.writelines("Node,Existence_score\n")
            for key in pathway_list.keys():
                f.writelines(f"{compound_name[key]},{compound_dict[key]}\n")
    else:
        print("Invalid directory name")
        sys.exit()
