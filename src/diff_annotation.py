import os
import sys
import pandas as pd

if __name__ == "__main__":
    from util import *
else:
    from .util import *
 
# check argument
assert len(sys.argv) == 3, \
    "Invalid arguments. Your current input is: " + sys.argv

# python file path
abs_dir = os.path.dirname(__file__)

try:
    data_1 = pd.read_csv(sys.argv[1])
    data_2 = pd.read_csv(sys.argv[2])
except FileNotFoundError:
    print(f"Cannot find the file")
    sys.exit()

data_merged = pd.merge(data_1, data_2, on=["ID", "start", "end"], how="outer")
data_merged.to_csv(create_savename(abs_dir, "merged"), index=False)