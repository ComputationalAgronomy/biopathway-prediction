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
enzyme_id = sys.argv[1] # add enyzme_id to the converted fasta 
name = sys.argv[2] # orignal protein fasta


def add_id(line):
    element = line.split("|")
    id = element[1]
    result = re.search(" (.*) OS=(.*) OX=.* PE=(\d)", element[2])
    product = result.group(1)
    organism = result.group(2)
    existence = result.group(3)
    gene = re.search("GN=(.*) PE=", element[2])
    if gene is not None:
        gene = gene.group(1)
    # >(id) (product)
    return f">{id} {enzyme_id}_{product}_{organism}_{existence}_{gene}"
    
def convert_fasta(filename):
    """This function converts uniprot fasta to prokka database format"""
    try:
        line = []
        with open(filename, "w+") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    read_line = read_line.strip("\n")
                    read_line = add_id(read_line)
                    # newline
                    try:
                        line[-1][1] += "\n"
                    except:
                        pass
                    line.append([read_line])
                    line[-1].append("")
            return line
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")


if os.path.isdir(name):
    # find fasta files in the directory
    file_list = glob.glob(os.path.join(name, "**/*.fasta"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    new_folder = True
    for filename in tqdm(file_list):
        line = convert_fasta(filename)
        with open(create_savename(abs_dir, filename,
                                  new_folder=new_folder), "w") as f:
            # concatenate all the entries
            j = ["\n".join(i) for i in line]
            f.writelines(j)
        new_folder = False 
elif os.path.isfile(name):
    line= convert_fasta(name)
    with open(create_savename(abs_dir, name), "w") as f:
            # concatenate all the entries
            j = ["\n".join(i) for i in line]
            f.writelines(j)
else:
    print("Invalid file or directory name")
    sys.exit()