import argparse
import glob
import os
import re
import time

import tomli
from tqdm import tqdm

from src.best_blast import find_best_blast
from src.match_enzyme import run_match_enzyme
from src.parse_ncbi_xml import parse_blast
from src.run_scripts import cpu_num, run_blast, run_prodigal
from src.util import make_dir

def parse_blast_(output_dir, input_folder):
    file_list = glob.glob(os.path.join(input_folder, "*.xml"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    parse_blast_folder = os.path.join(output_dir, "tmp/parse_blast")
    make_dir(parse_blast_folder)
    print("Parse blastp result")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        basename = re.sub(".xml", ".csv", basename)
        output_name = os.path.join(parse_blast_folder, basename)
        parse_blast(filename, output_name)
    print("Done!")

def find_best_blast_(output_dir, input_folder, criteria):
    file_list = glob.glob(os.path.join(input_folder, "*.csv"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    best_blast_folder = os.path.join(output_dir, "tmp/best_blast")
    make_dir(best_blast_folder)
    print("Select the best blastp result based on the configuration")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        output_name = os.path.join(best_blast_folder, basename)
        find_best_blast(filename, output_name, criteria=criteria)
    print("Done!")

def match_enzyme_(output_dir, input_folder):
    file_list = glob.glob(os.path.join(input_folder, "*.csv"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    enzyme_mapping_folder = os.path.join(output_dir, "result")
    make_dir(enzyme_mapping_folder)
    print("Match the best blastp result to enzyme pathway")
    for filename in tqdm(file_list):
        basename = os.path.basename(filename)
        basename = re.search("(.*).csv", basename).group(1)
        output_name = os.path.join(enzyme_mapping_folder, f"{basename}.txt")
        print(f"\n--------{basename}--------")
        run_match_enzyme(filename, output_name)
    print("Done!")

ROOT_DIR= os.path.dirname(__file__)

def main():
    # count total execution time
    time_start = time.time()

    parser = argparse.ArgumentParser()
    # without subcommand:
    # a positional argument to the path of the data
    parser.add_argument("datapath", type=str, help="input a file or directory path")
    # --debug not yet implemented
    parser.add_argument("--debug", action="store_true",
                        help="keep tmp folder if specified")
    parser.set_defaults(func=main)
    
    # with subcommand: run individual module
    subparser = parser.add_subparsers(help="module name")
    prodigal_parser = subparser.add_parser("prodigal")
    prodigal_parser.add_argument("input", help="[input_path]")
    prodigal_parser.set_defaults(func=run_prodigal_module)

    blast_parser = subparser.add_parser("blastp")
    blast_parser.add_argument("input", nargs="*",
                              help="[input_path] [optional:database_path]")
    blast_parser.set_defaults(func=run_blast_module)

    xml_parser = subparser.add_parser("parse_xml")
    xml_parser.add_argument("input", help="[input_path]")
    xml_parser.set_defaults(func=parse_blast_module)

    best_blast_parser = subparser.add_parser("best_blast")
    best_blast_parser.add_argument("input", nargs="*",
                                   help="[input_path] [optional:criteria]")
    best_blast_parser.set_defaults(func=find_best_blast_module)

    match_enzyme_parser = subparser.add_parser("match_enzyme")
    match_enzyme_parser.add_argument("input", help="[input_path]")
    match_enzyme_parser.set_defaults(func=match_enzyme_module)

    args = parser.parse_args()
    args.func(args)

    # TODO: finish calling module funcs 

    # read config
    with open(os.path.join(ROOT_DIR, "config.toml"), "rb") as f:
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
    prodigal_folder = os.path.join(ROOT_DIR, "tmp/prodigal")
    blast_folder = os.path.join(ROOT_DIR, "tmp/blast")
    # check available threads
    cpus = cpu_num()
    # run prodigal gene prediction
    run_prodigal(args.file, prodigal_folder)
    # run blastp protein alignment
    run_blast(prodigal_folder, blast_folder, database_path, cpus)
    
    # python functions
    # parse_blast
    parse_blast_(output_dir=ROOT_DIR, input_folder=blast_folder)

    # find_best_blast
    # default: find highest bit-score (column: score)
    # options: score, evalue, identity_percentage, query_coverage
    criteria = config["criteria"]["column"]
    find_best_blast(output_dir=ROOT_DIR,
                    input_folder=os.path.join(ROOT_DIR, "tmp/parse_blast"),
                    criteria=criteria)

    # match_enzyme
    match_enzyme_(output_dir=ROOT_DIR,
                  input_folder=os.path.join(ROOT_DIR, "tmp/best_blast"))

    time_end = time.time()
    print(f"Elapsed time: {round(time_end - time_start, 2)}sec")


if __name__ == "__main__":
    main()
