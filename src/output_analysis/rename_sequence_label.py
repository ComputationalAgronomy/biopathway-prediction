"""
This program will substitute the original downloaded sequence filename for
the species name. A file "filename_mapping.csv" will be saved to the current
path to tell what the filenames are changed to.

Usage
-----
$ python rename_sequence_label.py [input_dir] [file_extension_in_input_dir] 
  [optional: [rename_dir] [file_extension_in_rename_dir]]

Examples
--------
1. Rename the files in a folder containing downloaded sequences
$ python rename_sequence_label.py folder_with_sequences fna

2. Use the information in the downloaded sequences to rename other files
$ python rename_sequence_label.py folder_with_sequences fna \
  folder_with_files_to_be_renamed txt  

"""
import glob
import os
import re
import sys

import pandas as pd
from tqdm import tqdm

# python file path
DIR = os.path.dirname(__file__)

# non-greedy
REGEX_SPECIES = re.compile(r'seqhdr=\"(.*?)\"')

input_dir = sys.argv[1]
input_type = sys.argv[2]
try:
    rename_dir = sys.argv[3]
    rename_other_files = True
    rename_type = sys.argv[4]
except Exception:
    rename_other_files = False

mapping_dict = {}


def handle_weird_filename(str):
    return str.replace(",", "_").replace(" ", "_").replace(":", "_").replace("/", "_").strip("\n")


def get_files(dir, type):
    file_list = glob.glob(os.path.join(dir, f"**/*.{type}"), recursive=True)
    return file_list


def process_label_fna(filename):
    input_basename = os.path.basename(filename).rsplit(".", 1)[0]
    with open(filename, "r") as f:
        species_name = f.readline().split(" ", 1)[1]
        species_name = handle_weird_filename(species_name)
    return (input_basename, species_name)


def _process_label_prodigal(line):
    info = line.split(" ", 1)[1]
    species_name = REGEX_SPECIES.search(info).group(1)
    return species_name


def process_label_prodigal(filename):
    input_basename = os.path.basename(filename).rsplit(".", 1)[0]
    with open(filename, "r") as f:
        species_name = _process_label_prodigal(f.readline())
        species_name = handle_weird_filename(species_name)
    return (input_basename, species_name)


if os.path.isdir(input_dir):
    file_list = get_files(input_dir, input_type)
    for file in file_list:
        input_basename, species_name = process_label_fna(file)
        mapping_dict[input_basename] = species_name
    with open("filename_mapping.csv", "w") as f:
        for input_basename, species_name in mapping_dict.items():
            f.writelines(f"{input_basename},{species_name}\n")
    
    if rename_other_files:
        for file in get_files(rename_dir, rename_type):
            file_dir = os.path.dirname(file)
            basename, ext = os.path.basename(file).rsplit(".", 1)
            basename = handle_weird_filename(basename)
            try:
                new_file = os.path.join(file_dir, f"{mapping_dict[basename]}.{ext}")
                os.rename(file, new_file)
            except KeyError:
                pass
    else:
        for file in file_list:
            file_dir = os.path.dirname(file)
            basename, ext = os.path.basename(file).rsplit(".", 1)
            basename = handle_weird_filename(basename)
            new_file = os.path.join(file_dir, f"{mapping_dict[basename]}.{ext}")
            os.rename(file, new_file)
else:
    print("Invalid directory name")
    sys.exit()


