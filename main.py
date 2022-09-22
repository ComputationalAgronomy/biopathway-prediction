import os
import sys
import glob
import subprocess
import re
import argparse
from tqdm import tqdm
from src.run_scripts import run_blast, run_prodigal
from src.parse_ncbi_xml import parse_blast
from src.best_blast import find_best_blast
from src.match_enzyme import run_match_enzyme

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input a file or directory path")
    args = parser.parse_args()
    abs_dir = os.path.dirname(__file__)
    # shell scripts
    prodigal_folder = os.path.join(abs_dir, "tmp/prodigal")
    blast_folder = os.path.join(abs_dir, "tmp/blast")
    run_prodigal(args.file, prodigal_folder)
    run_blast(prodigal_folder, blast_folder)
    
    # python functions
    # parse_blast
    file_list = glob.glob(os.path.join(blast_folder, "*.xml"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    parse_blast_folder = os.path.join(abs_dir, "tmp/parse_blast")
    os.makedirs(parse_blast_folder)
    print("Parse blastp result")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        basename = re.sub(".xml", ".csv", basename)
        # basename = f"{os.path.basename(filename).split('.')[0]}.csv"
        output_name = os.path.join(parse_blast_folder, basename)
        parse_blast(filename, output_name)
    print("Done!")

    # find_best_blast
    file_list = glob.glob(os.path.join(parse_blast_folder, "*.csv"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    best_blast_folder = os.path.join(abs_dir, "tmp/best_blast")
    os.makedirs(best_blast_folder)
    print("Select the best blastp result based on the configuration")
    # default: find highest bit-score (column: score)
    # options: score, evalue, identity_percentage, query_coverage
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        # basename = f"{os.path.basename(filename).split('.')[0]}.csv"
        output_name = os.path.join(best_blast_folder, basename)
        find_best_blast(filename, output_name, criteria="score")
    print("Done!")

    # match_enzyme
    file_list = glob.glob(os.path.join(best_blast_folder, "*.csv"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    print("Match the best blastp result to enzyme pathway")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename).split('.')[0]
        print()
        print(f"--------{basename}--------")
        run_match_enzyme(filename)
    print("Done!")

if __name__ == "__main__":
    main()