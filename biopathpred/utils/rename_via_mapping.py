"""
This script will substitute filenames for the species name by using 
filename_mapping.csv generated from rename_sequence_label.py

Usage
-----
$ python rename_via_mapping.py RENAME_DIR FILE_EXTENSION_IN_RENAME_DIR MAPPING_FILE

Example
-------
$ python rename_via_mapping.py folder_with_files_to_be_renamed txt filename_mapping.csv

"""
import glob
import os
import sys

rename_dir = sys.argv[1]
rename_type = sys.argv[2]
mapping_file = sys.argv[3]

mapping_dict = {}


def handle_weird_filename(str):
    return str.replace(",", "_").replace(" ", "_").replace(":", "_").replace("/", "_").strip("\n")


def get_files(dir, type):
    file_list = glob.glob(os.path.join(dir, f"**/*.{type}"), recursive=True)
    return file_list


if os.path.isdir(rename_dir):
    file_list = get_files(rename_dir, rename_type)
    print(f"Find {len(file_list)} {rename_type} files.")
    with open(mapping_file, "r") as f:
        for line in f.readlines():
            input_basename, species_name = line.strip("\n").rsplit(",", 1)
            mapping_dict[input_basename] = species_name
    for file in file_list:
        file_dir = os.path.dirname(file)
        basename, ext = os.path.basename(file).rsplit(".", 1)
        basename = handle_weird_filename(basename)
        new_file = os.path.join(file_dir, f"{mapping_dict[basename]}.{ext}")
        os.rename(file, new_file)
        print(f"Rename {os.path.basename(file)} to {os.path.basename(new_file)}")
else:
    print("Invalid directory name")
    sys.exit()
