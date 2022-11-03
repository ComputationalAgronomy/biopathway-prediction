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
        self.load_default_config()
        
    def check_io(self, type, filetype=None):
        # This means we pipeline the results from the previous step, so self.type
        # has not yet been changed.
        if type != self.type:
            try:
                self.base_path
            except NameError:
                self.base_path = Configuration.check_output_path(self.args)
            self.input_path = self.output_path
            self.output_path = os.path.join(self.base_path, type)
            self.type = type
        else:
            # When this line is executed, we must be running a single module.
            # So set up for everything.
            self.input_path = self.args.input
            self.base_path = Configuration.check_output_path(self.args, module=True)
            self.output_path = os.path.join(self.base_path, type)
        
        # prodigal and blast scripts will handle this part
        if filetype is not None:
            self.file_list = Configuration.check_files_in_path(self.input_path, filetype)
            Configuration.make_dir(self.output_path)

        # check extra param
        self.check_param()

    def load_default_config(self):
        with open(os.path.join(ROOT_DIR, "config.toml"), "rb") as f:
            self.default = tomli.load(f)

    def check_param(self):
        if self.type == "blast":
            try:
                self.database = self.args.database
            except AttributeError:
                self.database = self.default["database"]["path"]
            Configuration.check_blast_database(self.database)
            self.thread_num = Configuration.thread_num()
        elif self.type == "best_blast":
            try:
                self.criteria = self.args.criteria
            except AttributeError:
                self.criteria = self.default["criteria"]["column"]

    @staticmethod
    def create_savename(filename, filetype):
        filename_no_extension = filename.rsplit(".", 1)[0]
        filename_new_extension = f"{filename_no_extension}.{filetype}"
        return filename_new_extension
   
    @staticmethod
    def check_output_path(args, module=False):
        try:
            return os.path.abspath(args.output)
        except AttributeError:
            if module:
                return os.path.join(ROOT_DIR, "module_output")
            else:
                return os.path.join(ROOT_DIR, "tmp")
    
    @staticmethod
    def make_dir(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
    
    @staticmethod
    def find_file(input_path, pattern):
        file_list = glob.glob(os.path.join(input_path, pattern), recursive=True)
        file_list = [file.replace("\\", "/") for file in file_list]
        return file_list

    @staticmethod
    def check_files_in_path(input_path, filetype):
        if os.path.isdir(input_path):
            pattern = f"*.{filetype}"
            file_list = Configuration.find_file(input_path, pattern)
        elif os.path.isfile(input_path):
            file_list = [input_path]
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
        res = subprocess.run("grep -c ^processor /proc/cpuinfo", shell=True,
                             stdout=subprocess.PIPE)
        return res.stdout  


# run individual modules
def run_parse_blast(config):
    config.check_io(type="parse_blast", filetype="xml")
    print("Parse blastp result")
    for filename in config.file_list:
        savename = Configuration.create_savename(filename, filetype="csv")
        parse_blast(filename=filename, output_filename=savename)
    print("Done!")

def run_find_best_blast(config):
    config.check_io(type="best_blast", filetype="csv")
    print("Select the best blastp result based on the configuration")
    for filename in config.file_list:
        savename = Configuration.create_savename(filename, filetype="csv")
        find_best_blast(filename=filename, output_filename=savename,
                        criteria=config.criteria)
    print("Done!")

def run_match_enzyme(config):
    config.check_io(type="match_enzyme", filetype="csv")
    print("Match the best blastp result to enzyme pathway")
    for filename in config.file_list:
        savename = config.create_savename(filetype="txt")
        _run_match_enzyme(filename=filename, output_filename=savename)
    print("Done!")


def parse_arguments():
    parser = argparse.ArgumentParser()
    # without subcommand:
    # a positional argument to the path of the data
    parser.add_argument("-i", "--input", type=str, help="input a file or directory path")
    parser.add_argument("-o", "--output", type=str, help="output path")
    parser.add_argument("-db", "--database", type=str, help="database path")
    # --debug not yet implemented
    parser.add_argument("--debug", action="store_true",
                        help="keep tmp folder if specified")
    parser.set_defaults(func=main, type="main")
    
    # with subcommand: run individual module
    subparser = parser.add_subparsers(help="module name")
    prodigal_parser = subparser.add_parser("prodigal")
    prodigal_parser.add_argument("input", type=str, help="input path")
    prodigal_parser.add_argument("-o", "--output", type=str, help="output path")
    prodigal_parser.set_defaults(func=run_prodigal_module, type="prodigal")

    blast_parser = subparser.add_parser("blastp")
    blast_parser.add_argument("input", type=str, help="input path")
    blast_parser.add_argument("-o", "--output", type=str, help="output path")
    blast_parser.add_argument("-db", "--database", type=str, help="database path")                             
    blast_parser.set_defaults(func=run_blast_module, type="blast")

    xml_parser = subparser.add_parser("parse_xml")
    xml_parser.add_argument("input", type=str, help="input path")
    xml_parser.add_argument("-o", "--output", type=str, help="output path")
    xml_parser.set_defaults(func=parse_blast_module, type="parse_blast")

    best_blast_parser = subparser.add_parser("best_blast")
    best_blast_parser.add_argument("input", type=str, help="input path")
    best_blast_parser.add_argument("-o", "--output", type=str, help="output path")
    best_blast_parser.add_argument("-c", "--criteria", type=str, help="selection criteria")
    best_blast_parser.set_defaults(func=find_best_blast_module, type="best_blast")

    match_enzyme_parser = subparser.add_parser("match_enzyme")
    match_enzyme_parser.add_argument("input", type=str, help="input path")
    match_enzyme_parser.add_argument("-o", "--output", type=str, help="output path")
    match_enzyme_parser.set_defaults(func=match_enzyme_module, type="match_enzyme")

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
