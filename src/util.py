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
        output_filename = os.path.join(abs_dir,
                                       create_folder(abs_dir, "output"),
                                       f"{filename}_{filenum}.csv")
    else:
        output_filename = re.sub(f"_(\d+)\.csv$", filenum, output_filename)
    if not os.path.exists(output_filename):
        return output_filename
    else:
        return create_savename(abs_dir, filename, filenum + 1)


