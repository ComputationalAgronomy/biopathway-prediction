import glob
import os
import statistics as st
import sys

import pandas as pd
from tqdm import tqdm

total_compound_dict = {}
total_enzyme_dict = {}

class Result():
    total_compound_dict = {}
    total_enzyme_dict = {}

    def __init__(self, filename):
        self.get_name(filename)
        self.compound_dict = {}
        self.enzyme_dict = {}
        self.parse_result(filename)

    def get_name(self, filename):
        self.name = os.path.basename(filename)

    def parse_result(self, filename):
        count_compound, count_enzyme = False, False
        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip("\n")
                if line == "Compound list:":
                    count_compound, count_enzyme = True, False
                    continue
                elif line == "Enzyme list:":
                    count_compound, count_enzyme = False, True
                    continue
                elif line == "":
                    continue
                else:
                    if count_compound:
                        self.extract_values(line, "compound")
                    elif count_enzyme:
                        self.extract_values(line, "enzyme")

    def extract_values(self, line, type):
        id_, score = line.split(": ")[0:2]
        try:
            score = float(score)
        except ValueError:
            score = float(score == "True")
        if type == "compound":
            try:
                self.compound_dict[id_] = score
                total_compound_dict[id_].append(score)
            except KeyError:
                total_compound_dict[id_] = [score]
        elif type == "enzyme":
            try:
                self.enzyme_dict[id_] = score
                total_enzyme_dict[id_].append(score)
            except KeyError:
                total_enzyme_dict[id_] = [score]


def write_summary(data_dict, type, output_path):
    """
    Write common statistics (max, min, mean and stdev) of input data to a csv
    file

    Parameters
    ----------
    data_dict : dict
        A dictionary that contains multiple lists of values
    
    type : str
        The type of data. This will be used as part of the output filename.

    """
    with open(os.path.join(output_path, f"{type}_output.csv"), "w") as f:
        f.writelines(f"{type}_key,{type}_value,max,min,mean,stdev\n")
        for key, value in data_dict.items():
            f.writelines(f"{key},{sum(value)},{max(value)},"
                         f"{min(value)},{st.mean(value)},{st.stdev(value)}\n")


def write_prediction(result_list, output_path):
    """
    Write prediction output to a csv file
    Current prediction value: the score of compound "iaa"

    Parameters
    ----------
    result_list : list
        A list containing Result objects
    
    """
    with open(os.path.join(output_path, f"prediction_output.csv"), "w") as f:
        f.writelines(f"species,score\n")
        for obj in result_list:
            species = obj.name.rsplit(".", 1)[0]
            score = obj.compound_dict["iaa"]
            f.writelines(f"{species},{score}\n")


def enzyme_mapping_analysis(path, output_path):
    result_list = []
    Result.total_compound_dict = {}
    Result.total_enzyme_dict = {}
    if os.path.isdir(path):
        file_list = glob.glob(os.path.join(path, "**/*.txt"), recursive=True)
        for filename in tqdm(file_list):
            result_list.append(Result(filename))
        write_summary(total_compound_dict, "compound", output_path)
        write_summary(total_enzyme_dict, "enzyme", output_path)
        result_list.sort(
            key=lambda obj: obj.compound_dict["iaa"], reverse=True)
        write_prediction(result_list, output_path)
    else:
        raise Exception(f"Invalid directory name: {path}")


if __name__ == "__main__":
    # python file path
    path = sys.argv[1]
    output_path = os.path.dirname(__file__)
    enzyme_mapping_analysis(path, output_path)
