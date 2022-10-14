import argparse
from genericpath import isfile
import glob
import os
import re
from tabnanny import check
import time

import tomli
from tqdm import tqdm

from src.best_blast import find_best_blast
from src.match_enzyme import _run_match_enzyme
from src.parse_ncbi_xml import parse_blast
from src.run_scripts import cpu_num, run_blast, run_prodigal
from src.util import make_dir, find_file


ROOT_DIR = os.path.dirname(__file__)
PRODIGAL_FOLDER = os.path.join(ROOT_DIR, "tmp/prodigal")
BLAST_FOLDER = os.path.join(ROOT_DIR, "tmp/blast")
PARSE_BLAST_FOLDER = os.path.join(ROOT_DIR, "tmp/parse_blast")
BEST_BLAST_FOLDER = os.path.join(ROOT_DIR, "tmp/best_blast")
ENZYME_MAPPING_FOLDER = os.path.join(ROOT_DIR, "result")

# utils
def load_config():
    with open(os.path.join(ROOT_DIR, "config.toml"), "rb") as f:
        config = tomli.load(f)
    return config

def check_blast_database(database_path):
    print("Check blast database existence")
    if os.path.isfile(database_path):
        print(f"Database: {os.path.basename(database_path)}")
    else:
        raise Exception("Blast database does not exist. Check config.toml before running.")

def run_and_save(func, output_path, file_list, file_save_format, **kwargs):
    for filename in tqdm(file_list):
        basename_old_extension = os.path.basename(filename)
        basename = basename_old_extension.rsplit(".", 1)[0]
        basename_new_extension = f"{basename}.{file_save_format}"
        output_name = os.path.join(output_path, basename_new_extension)
        func(filename, output_name, kwargs)        

# run individual modules
def run_parse_blast(input_path, output_path):
    if os.path.isdir(input_path):
        file_list = find_file(input_path, "*.xml")
    elif os.path.isfile(input_path):
        file_list = input_path
    make_dir(output_path)
    print("Parse blastp result")
    run_and_save(func=parse_blast, output_path=output_path,
                 file_list=file_list, file_save_format="csv")
    print("Done!")

def run_find_best_blast(input_path, output_path, criteria):
    if os.path.isdir(input_path):
        file_list = find_file(input_path, "*.csv")
    elif os.path.isfile(input_path):
        file_list = input_path
    make_dir(output_path)
    print("Select the best blastp result based on the configuration")
    run_and_save(func=find_best_blast, output_path=output_path,
                 file_list=file_list, file_save_format="csv", criteria=criteria)
    print("Done!")

def run_match_enzyme(input_path, output_path):
    if os.path.isdir(input_path):
        file_list = find_file(input_path, "*.csv")
    elif os.path.isfile(input_path):
        file_list = input_path
    make_dir(output_path)
    print("Match the best blastp result to enzyme pathway")
    run_and_save(func=_run_match_enzyme, output_path=output_path,
                 file_list=file_list, file_save_formet="txt")
    print("Done!")

# handle subparser arguments before running individule modules
def run_prodigal_module(args):
    output_path = os.path.join(ROOT_DIR, "module_output/prodigal")
    run_prodigal(input_path=args.input, output_path=output_path)

def run_blast_module(args):
    input_path = args.input[0]
    try:
        database_path = args.input[1]
    except IndexError:
        # load config
        config = load_config()
        database_path = config["database"]["path"]
    check_blast_database(database_path)

    output_path = os.path.join(ROOT_DIR, "module_output/blast")
    run_blast(input_path=input_path, output_path=output_path,
              database_path=database_path, cpus=cpu_num())

def parse_blast_module(args):
    input_path = args.input
    output_path = os.path.join(ROOT_DIR, "module_output/parse_blast")
    run_parse_blast(input_path=input_path, output_path=output_path)

def find_best_blast_module(args):
    input_path = args.input[0]
    output_path = os.path.join(ROOT_DIR, "module_output/best_blast")
    try:
        criteria = args.input[1]
    except IndexError:
        # load config
        config = load_config()
        criteria = config["criteria"]["column"]
    run_find_best_blast(input_path=input_path, output_path=output_path,
                        criteria=criteria)

def match_enzyme_module(args):
    input_path = args.input
    output_path = os.path.join(ROOT_DIR, "module_output/match_enzyme")
    run_match_enzyme(input_path=input_path, output_path=output_path)

def parse_arguments():
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
    
    return args

def main():
    # count total execution time
    time_start = time.time()

    # load config from config.toml
    config = load_config()
    
    # check blast database existence before running
    database_path = config["database"]["path"]
    check_blast_database(database_path)

    # shell scripts
    # check available threads
    cpus = cpu_num()
    # run prodigal gene prediction
    run_prodigal(input_path=args.file, output_path=PRODIGAL_FOLDER)
    # run blastp protein alignment
    run_blast(input_path=PRODIGAL_FOLDER, output_path=BLAST_FOLDER,
              database_path=database_path, cpus=cpus)
    
    # python functions
    # parse_blast
    run_parse_blast(input_path=BLAST_FOLDER, output_path=PARSE_BLAST_FOLDER)

    # find_best_blast
    # default: find highest bit-score (column: score)
    # options: score, evalue, identity_percentage, query_coverage
    criteria = config["criteria"]["column"]
    run_find_best_blast(input_path=PARSE_BLAST_FOLDER,
                        output_path=BEST_BLAST_FOLDER,
                        criteria=criteria)

    # match_enzyme
    run_match_enzyme(input_path=BEST_BLAST_FOLDER,
                     output_path=ENZYME_MAPPING_FOLDER)

    time_end = time.time()
    print(f"Elapsed time: {round(time_end - time_start, 2)}sec")


if __name__ == "__main__":
    args = parse_arguments()
    args.func(args)
