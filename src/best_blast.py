if __name__ == "__main__":
    from util import *
    import os
    import sys
    import glob
    import pandas as pd
    from tqdm import tqdm
else:
    import pandas as pd
    from .util import *


abs_dir = os.path.dirname(__file__)
assert len(sys.argv) == 3, "Invalid arguments"
name = sys.argv[1]
# score,evalue,identity_percentage,query_coverage
criteria = sys.argv[2]

def find_best_blast(filename, criteria):
    file = pd.read_csv(filename)
    data = file.loc[file.groupby(["id"])[criteria].idxmax()]
    return data

if __name__ == "__main__":
    if os.path.isdir(name):
        # find fasta files in the directory
        file_list = glob.glob(os.path.join(name, "**/*.csv"), recursive=True)
        file_list = [file.replace("\\", "/") for file in file_list]
        new_folder = True
        for filename in tqdm(file_list):
            output = create_savename(abs_dir, filename,
                                    new_folder=new_folder)
            best = find_best_blast(filename, criteria)
            best.to_csv(output, index=False)
    elif os.path.isfile(name):
        output = create_savename(abs_dir, name)
        best = find_best_blast(name, criteria)
        best.to_csv(output, index=False)
    else:
        print("Invalid file or directory name")
        sys.exit()

