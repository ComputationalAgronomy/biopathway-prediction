import pandas as pd
from .util import *

def parse_filter(filter):
    if not isinstance(filter, list):
        raise Exception("The filter for best_blast should be in a list format")
    filter_dict = {}
    for filter_item in filter:
        try:
            column, threshold = filter_item.split("=")
            filter_dict[column] = float(threshold)
        except ValueError:
            print("The filter should have the following format '[column]=[threshold]'")
    return filter_dict

def find_best_blast(filename, output_filename, criteria="score", filter=None):
    file = pd.read_csv(filename)
    # filter the best result in each group (gene_prediction_id)
    data = file.loc[file.groupby(["id"])[criteria].idxmax()]
    filter = parse_filter(filter)
    if filter:
        for filter_key, filter_value in filter.items():
            data = data.loc[data[filter_key] >= filter_value]
        # data = data.loc[data["identity"] >= 40]
    data.to_csv(output_filename, index=False)
