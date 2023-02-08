import glob
import os
import sys

import matplotlib.pyplot as plt


def parse_filename(filename):
    basename = os.path.basename(filename).rsplit(".", 1)[0]
    copy_number = basename.split("_")[1]
    identity = basename.split("_")[3]
    return copy_number, identity


def parse_result(filename):
    copy_number, identity = parse_filename(filename)
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip("\n")
            if not line.startswith("iaa"):
                continue
            iaa_value = float(line.split(" ")[1])
            break
    return {"copy_number": copy_number, "identity": identity,
            "iaa_value": iaa_value}


def find_file(input_path, pattern):
    file_list = glob.glob(os.path.join(input_path, pattern), recursive=True)
    return file_list


def analyze_model_test_result(folder_path):
    files = find_file(folder_path, "copy_1_*.txt")
    result_collection = []
    for file in files:
        result_collection.append(parse_result(file))

    axis_identity = [result["identity"] for result in result_collection]
    axis_iaa = [result["iaa_value"] for result in result_collection]
    plt.rcParams['figure.figsize'] = (10, 10)
    plt.plot(axis_identity, axis_iaa)
    plt.show()


if __name__ == "__main__":
    folder_path = sys.argv[1]
    analyze_model_test_result(folder_path)
