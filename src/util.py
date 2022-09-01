import os
import re

def create_folder(abs_dir, foldername, foldernum=1):
    "This function will create a folder if the folder name specified doesn't exist"
    if foldernum > 100:
        print("too many folders")
    folder_path = os.path.join(abs_dir, foldername)
    if os.path.exists(folder_path):
        foldername = re.sub("_(\d+)$", f"_{str(foldernum + 1)}", foldername)
        create_folder(abs_dir, foldername, foldernum + 1)
    else:
        os.makedirs(folder_path)
        return foldername

# [directory_name]/[filename]_[filenum].csv
def create_savename(abs_dir, filename, filenum=1, new_folder=True):
    """This function will create a proper filename for the output file"""
    if filenum == 1:
        filename = os.path.basename(filename).split(".")[0]
        if new_folder:
            foldername = create_folder(abs_dir, "output_1")
        filename = os.path.join(abs_dir,
                                foldername,
                                f"{filename}_{filenum}.csv")
    else:
        filename = re.sub("_(\d+)\.csv$", f"_{str(filenum)}.csv", filename)
    if not os.path.exists(filename):
        return filename
    else:
        return create_savename(abs_dir, filename, filenum + 1)


