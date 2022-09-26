import os
import glob
import time
import re
import argparse
import tomli
from tqdm import tqdm
from src.run_scripts import run_blast, run_prodigal, cpu_num
from src.parse_ncbi_xml import parse_blast
from src.best_blast import find_best_blast
from src.match_enzyme import run_match_enzyme
from src.util import make_dir

def main():
    time_start = time.time()
    abs_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input a file or directory path")
    # --debug not yet implemented
    parser.add_argument("--debug", action="store_true",
                        help="keep tmp folder if specified")
    args = parser.parse_args()

    # read config
    with open(os.path.join(abs_dir, "config.toml"), "rb") as f:
        config = tomli.load(f)
    
    # check blast database existence before running
    database_path = config["database"]["path"]
    # if a relative path is given, the current folder equals that in terminal
    print("Check blast database existence")
    if os.path.isfile(database_path):
        print(f"Database: {os.path.basename(database_path)}")
    else:
        print("Blast database does not exist. Check config.toml before running.")

    # shell scripts
    prodigal_folder = os.path.join(abs_dir, "tmp/prodigal")
    blast_folder = os.path.join(abs_dir, "tmp/blast")
    cpus = cpu_num()
    # run prodigal gene prediction
    run_prodigal(args.file, prodigal_folder)
    # run blastp protein alignment
    run_blast(prodigal_folder, blast_folder, database_path, cpus)
    
    # python functions
    # parse_blast
    file_list = glob.glob(os.path.join(blast_folder, "*.xml"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    parse_blast_folder = os.path.join(abs_dir, "tmp/parse_blast")
    make_dir(parse_blast_folder)
    print("Parse blastp result")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        basename = re.sub(".xml", ".csv", basename)
        output_name = os.path.join(parse_blast_folder, basename)
        parse_blast(filename, output_name)
    print("Done!")

    # find_best_blast
    file_list = glob.glob(os.path.join(parse_blast_folder, "*.csv"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    best_blast_folder = os.path.join(abs_dir, "tmp/best_blast")
    make_dir(best_blast_folder)
    print("Select the best blastp result based on the configuration")
    # default: find highest bit-score (column: score)
    # options: score, evalue, identity_percentage, query_coverage
    criteria = config["criteria"]["column"]
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        output_name = os.path.join(best_blast_folder, basename)
        find_best_blast(filename, output_name, criteria=criteria)
    print("Done!")

    # match_enzyme
    file_list = glob.glob(os.path.join(best_blast_folder, "*.csv"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    enzyme_mapping_folder = os.path.join(abs_dir, "result")
    make_dir(enzyme_mapping_folder)
    print("Match the best blastp result to enzyme pathway")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        basename = re.search("(.*).csv", basename).group(1)
        output_name = os.path.join(enzyme_mapping_folder, f"{basename}.txt")
        print(f"\n--------{basename}--------")
        run_match_enzyme(filename, output_name)
    print("Done!")
    time_end = time.time()
    print(f"Elapsed time: {round(time_end - time_start, 2)}sec")


if __name__ == "__main__":
    main()