from ast import arg
import os
import glob
import time
import re
import argparse
import threading
from tqdm import tqdm
from src.run_scripts import run_blast, run_prodigal
from src.parse_ncbi_xml import parse_blast
from src.best_blast import find_best_blast
from src.match_enzyme import run_match_enzyme

def main():
    time_start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input a file or directory path")
    parser.add_argument("--debug", action="store_true",
                        help="keep tmp folder if specified")
    parser.add_argument("--time", action="store_true", help="count time elapsed")
    args = parser.parse_args()
    abs_dir = os.path.dirname(__file__)
    # shell scripts
    prodigal_folder = os.path.join(abs_dir, "tmp/prodigal")
    blast_folder = os.path.join(abs_dir, "tmp/blast")
    run_prodigal(args.file, prodigal_folder)
    run_blast(prodigal_folder, blast_folder)

    prodigal_list = glob.glob(os.path.join(prodigal_folder, "*.faa"), recursive=True)
    prodigal_list = [file.replace("\\", "/") for file in file_list]
    for file in prodigal_list:
        predicted_count = 0
        with open(file, "r") as f:
            for line in f.readlines():
                if line.startswith(">"):
                    predicted_count += 1
        thread_blast = threading.Thread(target=run_blast, args=[file, blast_folder])
        thread_blast.start()
        blast_output_basename = re.sub(".faa", ".xml", file)
        blast_output_name = os.path.join(blast_folder, blast_output_basename)
        if os.path.exists(blast_output_name):
            last_entry = re.search(".*<Iteration_query-def>([^ ]*)",
                                   blast_output_name).group(1)
        

    thread_1.join()

    # python functions
    # parse_blast
    file_list = glob.glob(os.path.join(blast_folder, "*.xml"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    parse_blast_folder = os.path.join(abs_dir, "tmp/parse_blast")
    if not os.path.isdir(parse_blast_folder):
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
    if not os.path.isdir(best_blast_folder):
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
        basename = re.search("(.*).csv", filename).group(1)
        print()
        print(f"--------{basename}--------")
        run_match_enzyme(filename)
    print("Done!")
    time_end = time.time()
    print(f"Elapsed time: {round(time_end - time_start, 2)}")


if __name__ == "__main__":
    main()