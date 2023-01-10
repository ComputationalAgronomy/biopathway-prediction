"""
This program will substitute the original downloaded sequence filename for
species name. 
"""
import glob
import os
import sys

import pandas as pd
from tqdm import tqdm

# python file path
DIR = os.path.dirname(__file__)

input_dir = sys.argv[1]
input_type = sys.argv[2]
try:
    rename_dir = sys.argv[3]
    rename_other_files = True
except Exception:
    pass

mapping_dict = {}

def get_files(dir, type):
    file_list = glob.glob(os.path.join(dir, f"**/*.{type}"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    return file_list


def process_label(filename):
    input_basename = os.path.basename(filename).rsplit(".", 1)[0]
    with open(filename, "r") as f:
        species_name = f.readline().split(" ", 1)[1]
        species_name = species_name.replace(",", "_").replace(" ", "_").replace(":", "_").replace("/", "_").strip("\n")
    return (input_basename, species_name)


if os.path.isdir(input_dir):
    file_list = get_files(input_dir, input_type)
    for file in file_list:
        input_basename, species_name = process_label(file)
        mapping_dict[input_basename] = species_name
    with open("filename_mapping.csv", "w") as f:
        for input_basename, species_name in mapping_dict.items():
            f.writelines(f"{input_basename},{species_name}\n")
    
    filetype = "txt"
    if rename_other_files:
        for file in get_files(rename_dir, filetype):
            file_dir = os.path.dirname(file)
            basename, ext = os.path.basename(file).rsplit(".", 1)
            basename = basename.replace(",", "_").replace(" ", "_").replace(":", "_").replace("/", "_").strip("\n")
            try:
                new_file = os.path.join(file_dir, f"{mapping_dict[basename]}.{ext}")
                os.rename(file, new_file)
            except KeyError:
                pass
    else:
        for file in file_list:
            file_dir = os.path.dirname(file)
            basename, ext = os.path.basename(file).rsplit(".", 1)
            basename = basename.replace(",", "_").replace(" ", "_").replace(":", "_").replace("/", "_").strip("\n")
            new_file = os.path.join(file_dir, f"{mapping_dict[basename]}.{ext}")
            os.rename(file, new_file)
else:
    print("Invalid directory name")
    sys.exit()


