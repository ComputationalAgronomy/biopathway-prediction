import argparse
import os
import time

import tomli
from tqdm import tqdm

from src.best_blast import find_best_blast
from src.match_enzyme import _run_match_enzyme
from src.parse_ncbi_xml import parse_blast
from src.run_scripts import run_blast, run_prodigal

ROOT_DIR = os.path.dirname(__file__)

import glob
import subprocess

class Configuration():
    def __init__(self, args):
        self.args = args
        self.type = args.type
        self.__module = False if self.type == "main" else True
        self.filetype_dict = {"parse_blast": {"input": "xml", "output": "csv"},
                              "best_blast": {"input": "csv", "output": "csv"},
                              "match_enzyme": {"input": "csv", "output": "txt"}}
        self.load_default_config()
        
    def check_io(self, type):
        # This means we pipeline the results from the previous step, so self.type
        # has not yet been changed.
        if type != self.type and self.type != "main":
            try:
                self.base_path
            except AttributeError:
                self.get_base_path()
            self.input_path = self.output_path
        else:
            self.input_path = self.args.input
            self.get_base_path()
        self.output_path = os.path.join(self.base_path, type)
        self.type = type
        
        # prodigal and blast scripts will handle this part
        # check input filetype
        try:
            self.filetype_dict[type]
            self.file_list = self.check_files_in_path()
            os.makedirs(self.output_path, exist_ok=True)
        except KeyError:
            pass

        # check extra param
        self.check_param()

    def load_default_config(self):
        with open(os.path.join(ROOT_DIR, "config.toml"), "rb") as f:
            self.default = tomli.load(f)

    def check_param(self):
        if self.type == "blast":
            self.database = self.args.database
            if self.database is None:
                self.database = self.default["database"]["path"]
            Configuration.check_blast_database(self.database)
            self.thread_num = Configuration.thread_num()
        elif self.type == "best_blast":
            self.criteria = self.args.criteria
            if self.criteria is None:
                self.criteria = self.default["criteria"]["column"]

    def get_base_path(self):
        try:
            self.base_path = os.path.abspath(self.args.output)
        except TypeError:
            if self.__module:
                self.base_path = os.path.join(ROOT_DIR, "module_output")
            else:
                self.base_path = os.path.join(ROOT_DIR, "tmp")

    def create_savename(self, filename):
        filetype = self.filetype_dict[self.type]["output"]
        basename = os.path.basename(filename)
        basename_no_extension = basename.rsplit(".", 1)[0]
        savename_no_extension = os.path.join(self.output_path, basename_no_extension)
        savename_new_extension = f"{savename_no_extension}.{filetype}"
        return savename_new_extension
    
    def check_files_in_path(self):
        input_path = self.input_path
        if os.path.isdir(input_path):
            filetype = self.filetype_dict[self.type]["input"]
            pattern = f"*.{filetype}"
            file_list = Configuration.find_file(input_path, pattern)
        elif os.path.isfile(input_path):
            file_list = [input_path]
        return file_list

    @staticmethod
    def find_file(input_path, pattern):
        file_list = glob.glob(os.path.join(input_path, pattern), recursive=True)
        file_list = [file.replace("\\", "/") for file in file_list]
        return file_list

    @staticmethod
    def check_blast_database(database_path):
        print("Check blast database existence")
        if os.path.isfile(database_path):
            print(f"Database: {os.path.basename(database_path)}")
        else:
            raise Exception("Blast database does not exist. Check config.toml before running.")
    
    @staticmethod
    def thread_num():
        return str(os.cpu_count())  


# run individual modules
def run_parse_blast(config):
    config.check_io(type="parse_blast")
    print("Parse blastp result")
    for filename in config.file_list:
        savename = config.create_savename(filename)
        parse_blast(filename=filename, output_filename=savename)
    print("Done!")

def run_find_best_blast(config):
    config.check_io(type="best_blast")
    print("Select the best blastp result based on the configuration")
    for filename in config.file_list:
        savename = config.create_savename(filename)
        find_best_blast(filename=filename, output_filename=savename,
                        criteria=config.criteria)
    print("Done!")

def run_match_enzyme(config):
    config.check_io(type="match_enzyme")
    print("Match the best blastp result to enzyme pathway")
    for filename in config.file_list:
        savename = config.create_savename(filename)
        _run_match_enzyme(filename=filename, output_filename=savename)
    print("Done!")


def parse_arguments():
    parser = argparse.ArgumentParser()
    # without subcommand:
    # a positional argument to the path of the data
    parser.add_argument("-i", "--input", type=str, help="input a file or directory path")
    parser.add_argument("-o", "--output", type=str, help="output path")
    parser.add_argument("-db", "--database", type=str, help="database path")
    parser.add_argument("-c", "--criteria", type=str, help="selection criteria")
    # --debug not yet implemented
    parser.add_argument("--debug", action="store_true",
                        help="keep tmp folder if specified")
    parser.set_defaults(func=main, type="main")
    
    # with subcommand: run individual module
    subparser = parser.add_subparsers(help="module name")
    prodigal_parser = subparser.add_parser("prodigal")
    prodigal_parser.add_argument("-i", "--input", type=str,
                                 help="input a file or directory path",
                                 required=True)
    prodigal_parser.add_argument("-o", "--output", type=str, help="output path")
    prodigal_parser.set_defaults(func=run_prodigal, type="prodigal")

    blast_parser = subparser.add_parser("blastp")
    blast_parser.add_argument("-i", "--input", type=str,
                              help="input a file or directory path",
                              required=True)
    blast_parser.add_argument("-o", "--output", type=str, help="output path")
    blast_parser.add_argument("-db", "--database", type=str, help="database path")
    blast_parser.set_defaults(func=run_blast, type="blast")

    xml_parser = subparser.add_parser("parse_xml")
    xml_parser.add_argument("-i", "--input", type=str,
                            help="input a file or directory path",
                            required=True)
    xml_parser.add_argument("-o", "--output", type=str, help="output path")
    xml_parser.set_defaults(func=run_parse_blast, type="parse_blast")

    best_blast_parser = subparser.add_parser("best_blast")
    best_blast_parser.add_argument("-i", "--input", type=str,
                                   help="input a file or directory path",
                                   required=True)
    best_blast_parser.add_argument("-o", "--output", type=str, help="output path")
    best_blast_parser.add_argument("-c", "--criteria", type=str, help="selection criteria")
    best_blast_parser.set_defaults(func=run_find_best_blast, type="best_blast")

    match_enzyme_parser = subparser.add_parser("match_enzyme")
    match_enzyme_parser.add_argument("-i", "--input", type=str,
                                     help="input a file or directory path",
                                     required=True)
    match_enzyme_parser.add_argument("-o", "--output", type=str, help="output path")
    match_enzyme_parser.set_defaults(func=run_match_enzyme, type="match_enzyme")

    args = parser.parse_args()
    
    return args

def main(config):
    # count total execution time
    time_start = time.time()

    # scripts
    # run prodigal gene prediction
    run_prodigal(config)
    # run blastp protein alignment
    run_blast(config)
    
    # python functions
    # parse_blast
    run_parse_blast(config)

    # find_best_blast
    # criteria default: find highest bit-score (column: score)
    # options: score, evalue, identity_percentage, query_coverage
    run_find_best_blast(config)

    # match_enzyme
    run_match_enzyme(config)

    time_end = time.time()
    print(f"Elapsed time: {round(time_end - time_start, 2)}sec")


if __name__ == "__main__":
    args = parse_arguments()
    config = Configuration(args)
    args.func(config)
