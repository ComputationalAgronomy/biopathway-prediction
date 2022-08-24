import os
import re

def create_folder(abs_dir, foldername):
    "This function will create a folder if the folder name specified doesn't exist"
    folder_path = os.path.join(abs_dir, foldername)
    if os.path.exists(folder_path):
        return foldername
    else:
        os.makedirs(folder_path)
        return foldername

# [directory_name]/[filename]_[filenum].csv
def create_savename(abs_dir, filename, filenum=1):
    """This function will create a proper filename for the output file"""
    if filenum == 1:
        filename = os.path.basename(filename).split(".")[0]
        foldername = "output"
        create_folder(abs_dir, foldername)
        filename = os.path.join(abs_dir,
                                "output",
                                f"{filename}_{filenum}.csv")
    else:
        filename = re.sub("_(\d+)\.csv$", f"_{str(filenum)}.csv", filename)
    if not os.path.exists(filename):
        return filename
    else:
        return create_savename(abs_dir, filename, filenum + 1)


