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
output_dir = sys.argv[2]


def get_files(dir, type):
    file_list = glob.glob(os.path.join(dir, f"**/*.{type}"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    return file_list


def process_label_and_match(filename, output_dir):
    output_dir = os.path.abspath(output_dir)
    txt_filename = os.path.basename(filename).rsplit(".", 1)[0]
    txt_filename = f"{txt_filename}.fna"
    txt_filename = os.path.join(output_dir, txt_filename)
    with open(filename, "r") as f:
        name = f.readline().split(" ", 1)[1]
        name = name.replace(",", "_").replace(" ", "_").replace(":", "_").strip("\n")
    try:
        os.rename(txt_filename, f"{os.path.join(output_dir, name)}.fna")
    except FileNotFoundError:
        pass

if os.path.isdir(input_dir) and os.path.isdir(output_dir):
    file_list = get_files(input_dir, "fna")
    for filename in tqdm(file_list):
        process_label_and_match(filename, output_dir)
else:
    print("Invalid directory name")
    sys.exit()
