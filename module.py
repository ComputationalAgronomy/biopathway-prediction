import os
import sys
import glob
import argparse
import re
import tomli
from src.run_scripts import run_blast, run_prodigal
from src.best_blast import find_best_blast
from src.parse_ncbi_xml import parse_blast
from src.match_enzyme import run_match_enzyme

def main():
    abs_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_prodigal", nargs=1, help="[input_path]")
    parser.add_argument("--run_blast", nargs="*",
                        help="[input_path] [optional:database_path]")
    parser.add_argument("--parse_ncbi_xml", nargs=1, help="[input_path]")
    parser.add_argument("--best_blast", nargs="*",
                        help="[input_path] [optional:criteria]")
    parser.add_argument("--match_enzyme", nargs=1, help="[input_path]")
    args = parser.parse_args()

    with open(os.path.join(abs_dir, "config.toml"), "rb") as f:
        config = tomli.load(f)

    output_path = os.path.join(abs_dir, "module_output")
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    if args.run_prodigal is not None:
        prodigal_output = os.path.join(output_path, "prodigal")
        run_prodigal(args.run_prodigal[0], prodigal_output)

    if args.run_blast is not None:
        blast_output = os.path.join(output_path, "blast")
        if len(args.run_blast) == 2:
            database_path = args.run_blast[1]
        elif len(args.run_blast) == 1:
            database_path = config["database"]["path"]
        else:
            print("Invalid arguments")
            sys.exit()
        run_blast(args.run_blast[0], blast_output, database_path)

    if args.parse_ncbi_xml is not None:
        parse_blast_folder = os.path.join(output_path, "parse_blast")
        if not os.path.isdir(parse_blast_folder):
            os.makedirs(parse_blast_folder)
        if os.path.isfile(args.parse_ncbi_xml[0]):
            filename = args.parse_ncbi_xml[0]
            basename = os.path.basename(filename)
            basename = re.sub(".xml", ".csv", basename)
            output_name = os.path.join(parse_blast_folder, basename)
            parse_blast(filename, output_name)
        else:
            file_list = glob.glob(os.path.join(args.parse_ncbi_xml[0], "*.xml"),
                                recursive=True)
            file_list = [file.replace("\\", "/") for file in file_list]
            for filename in file_list:
                basename = os.path.basename(filename)
                basename = re.sub(".xml", ".csv", basename)
                output_name = os.path.join(parse_blast_folder, basename)
                parse_blast(filename, output_name)

    if args.best_blast is not None:
        best_blast_folder = os.path.join(output_path, "best_blast")
        if not os.path.isdir(best_blast_folder):
            os.makedirs(best_blast_folder)
        if len(args.best_blast) == 2:
            database_path = args.best_blast[1]
        elif len(args.best_blast) == 1:
            # default: find highest bit-score (column: score)
            # options: score, evalue, identity_percentage, query_coverage
            criteria = config["criteria"]["column"]
        else:
            print("Invalid arguments")
            sys.exit()
        if os.path.isfile(args.best_blast[0]):
            filename = args.best_blast[0]
            basename = os.path.basename(filename)
            output_name = os.path.join(best_blast_folder, basename)
            find_best_blast(filename, output_name, criteria=criteria)
        else:
            file_list = glob.glob(os.path.join(args.best_blast[0], "*.csv"),
                                  recursive=True)
            file_list = [file.replace("\\", "/") for file in file_list]
            for filename in file_list:
                basename = os.path.basename(filename)
                output_name = os.path.join(best_blast_folder, basename)
                find_best_blast(filename, output_name, criteria=criteria)
    
    if args.match_enzyme is not None:
        enzyme_mapping_folder = os.path.join(output_path, "match_enzyme")        
        if not os.path.isdir(enzyme_mapping_folder):
            os.makedirs(enzyme_mapping_folder)
        if os.path.isfile(args.match_enzyme[0]):
            filename = args.match_enzyme[0]
            basename = os.path.basename(filename)
            basename = re.search("(.*).csv", basename).group(1)
            output_name = os.path.join(enzyme_mapping_folder, f"{basename}.txt")
            print(f"\n--------{basename}--------")
            run_match_enzyme(filename, output_name)    
        else:
            file_list = glob.glob(os.path.join(args.match_enzyme[0], "*.csv"),
                                recursive=True)
            file_list = [file.replace("\\", "/") for file in file_list]
            for filename in file_list:
                basename = os.path.basename(filename)
                basename = re.search("(.*).csv", basename).group(1)
                output_name = os.path.join(enzyme_mapping_folder, f"{basename}.txt")
                print(f"\n--------{basename}--------")
                run_match_enzyme(filename, output_name)

if __name__ == "__main__":
    main()
