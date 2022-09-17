import os
import sys
import re
import glob
from tqdm import tqdm

if __name__ == "__main__":
    from util import *
else:
    from .util import *



abs_dir = os.path.dirname(__file__)
assert len(sys.argv) == 3, "Invalid arguments"
name = sys.argv[1]
enzyme_id = sys.argv[2]

def add_id(line):
    element = line.split(" ", 1)
    product_info = element[1]
    return f"{element[0]} {enzyme_id}_{product_info}"
    
def split_fasta(filename):
    """This function will split different protein entries in database"""
    try:
        line = []
        with open(filename, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    read_line = read_line.strip("\n")
                    read_line = add_id(read_line)
                    # newline and check if the last entry exists
                    try:
                        line[-1][1] += "\n"
                    except:
                        pass
                    line.append([read_line])
                    line[-1].append("")
                else:
                    try:
                        # merge fasta sequence
                        line[-1][1] += read_line
                    except IndexError:
                        print("Error in input format")
                        return
            return line
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")


if os.path.isdir(name):
    # find fasta files in the directory
    file_list = glob.glob(os.path.join(name, "**/*.fasta"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    new_folder = True
    for filename in tqdm(file_list):
        line = split_fasta(filename)
        with open(create_savename(abs_dir, filename,
                                  new_folder=new_folder), "w") as f:
            # concatenate all the entries
            j = ["\n".join(i) for i in line]
            f.writelines(j)
        new_folder = False 
elif os.path.isfile(name):
    line = split_fasta(name)
    with open(create_savename(abs_dir, name), "w") as f:
            # concatenate all the entries
            j = ["\n".join(i) for i in line]
            f.writelines(j)
else:
    print("Invalid file or directory name")
    sys.exit()