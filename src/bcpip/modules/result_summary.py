from collections import defaultdict
from pathlib import Path
from typing import List, Literal

import numpy as np


class Result():
    """Parse and store the result from the output of match_enzyme module"""

    total_compound_dict = defaultdict(list)
    total_enzyme_dict = defaultdict(list)

    def __init__(self, filepath: Path):
        self.compound_dict = {}
        self.enzyme_dict = {}
        self.name = filepath.name
        self._parse_result(filepath)

    def _parse_result(self, filepath: Path):
        count_compound, count_enzyme = False, False
        with open(filepath, "r") as f:
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
                        self._extract_values(line, "compound")
                    elif count_enzyme:
                        self._extract_values(line, "enzyme")

    def _extract_values(self, line: str, type: Literal["compound", "enzyme"]):
        id_, score = line.split(": ")[0:2]
        try:
            score = float(score)
        except ValueError:
            score = float(score == "True")
        if type == "compound":
            self.compound_dict[id_] = score
            self.total_compound_dict[id_].append(score)
        elif type == "enzyme":
            self.enzyme_dict[id_] = score
            self.total_enzyme_dict[id_].append(score)


def write_summary(data_dict: dict, type: Literal["compound", "enzyme"], output_path: Path):
    """Write common statistics (max, min, mean and stdev) of input data to a csv
    file.

    Args:
        data_dict: A dictionary that contains multiple lists of values.
        type: The type of data, "compound" or "enzyme".
    """
    with open(output_path / f"{type}_output.csv", "w") as f:
        f.write(f"{type}_key,{type}_value,max,min,mean,stdev\n")
        for key, value in data_dict.items():
            f.write(f"{key},{round(sum(value), 6)},{max(value)},"
                    f"{min(value)},{round(np.mean(value), 6)},"
                    f"{round(np.std(value, ddof=1), 6)}\n")


def write_prediction(result_list: List[Result], output_path: Path):
    """Write prediction output to a csv file.

    The prediction output is the score of the compound "iaa".

    Args:
        result_list : A list containing Result objects.
    """
    with open(output_path / "prediction_output.csv", "w") as f:
        f.write("species,score\n")
        for obj in result_list:
            species = obj.name.rsplit(".", 1)[0]
            score = obj.compound_dict["iaa"]
            f.write(f"{species},{score}\n")


def result_summary(path: Path, output_path: Path):
    """Collect the match_enzyme results from a folder and summarize them.

    Args:
        path: The path to the folder containing match_enzyme results.
        output_path: The path to save the summary.
    """
    result_list = []
    # Reset the shared attributes
    Result.total_compound_dict = defaultdict(list)
    Result.total_enzyme_dict = defaultdict(list)

    file_list = path.glob("**/*.txt")
    for filepath in file_list:
        result_list.append(Result(filepath))
    write_summary(Result.total_compound_dict, "compound", output_path)
    write_summary(Result.total_enzyme_dict, "enzyme", output_path)
    # Sort by score then species name
    result_list.sort(
        key=lambda obj: (-obj.compound_dict["iaa"], obj.name.rsplit(".", 1)[0])
    )
    write_prediction(result_list, output_path)
