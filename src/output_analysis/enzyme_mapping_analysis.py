import os
import sys
import statistics as st
import glob
from tqdm import tqdm
import pandas as pd

# python file path
DIR = os.path.dirname(__file__)

name = sys.argv[1]

compound_dict = {}
enzyme_dict = {}


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
                        compound_dict[compound_id].append(exist)
                    except KeyError:
                        compound_dict[compound_id] = [exist]
                elif count_enzyme:
                    enzyme_id += 1
                    num = float(line.split(":")[1])
                    try:
                        enzyme_dict[enzyme_id].append(num)
                    except KeyError:
                        enzyme_dict[enzyme_id] = [num]

def write_output(dict, type):
    with open(os.path.join(DIR, f"{type}_output.csv"), "w") as f:
        f.writelines(f"{type}_key,{type}_value,max,min,mean,stdev\n")
        for key, value in dict.items():
            f.writelines(f"{key},{sum(value)},{max(value)},"
                         f"{min(value)},{st.mean(value)},{st.stdev(value)}\n")

if os.path.isdir(name):
    file_list = glob.glob(os.path.join(name, "**/*.txt"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    for filename in tqdm(file_list):
        parse_result(filename)
    write_output(compound_dict, "compound")
    write_output(enzyme_dict, "enzyme")
else:
    print("Invalid directory name")
    sys.exit()
