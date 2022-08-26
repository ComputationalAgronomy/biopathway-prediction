import os
import sys
import pandas as pd

if __name__ == "__main__":
    from util import *
else:
    from .util import *
 
# check argument
assert len(sys.argv) == 4, "Invalid arguments"

# python file path
abs_dir = os.path.dirname(__file__)

try:
    data_1 = pd.read_csv(sys.argv[2])
    data_2 = pd.read_csv(sys.argv[3])
except FileNotFoundError:
    print(f"Cannot find the file")
    sys.exit()

format = sys.argv[1]
if format == "--merge":
    method = ["ID", "start", "end"]
elif format == "--kofam":
    method = ["ID", "sequence_no"]
else:
    print("Invalid format")
    sys.exit()

data_merged = pd.merge(data_1, data_2, on=method, how="outer")
data_merged.to_csv(create_savename(abs_dir, "merged"), index=False)

