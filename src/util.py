import os
import re

# deprecated: recursion style
""" def create_folder(abs_dir, foldername, foldernum=1):
    This function will create a folder if the folder name specified doesn't exist
    if foldernum > 100:
        print("too many folders")
    folder_path = os.path.join(abs_dir, foldername)
    if os.path.exists(folder_path):
        foldername = re.sub("_(\d+)$", f"_{str(foldernum + 1)}", foldername)
        return create_folder(abs_dir, foldername, foldernum + 1)
    else:
        os.makedirs(folder_path)
        return foldername """

def create_folder(abs_dir, foldername, foldernum=1):
    """This function will create a folder if the folder name specified
       doesn't exist"""
    folder_path = os.path.join(abs_dir, foldername)
    while os.path.exists(folder_path):
        if foldernum > 100:
            raise Exception("A bug in creating a folder!")
        foldernum += 1
        foldername = re.sub("_(\d+)$", f"_{str(foldernum)}", foldername)
        folder_path = os.path.join(abs_dir, foldername)
    os.makedirs(folder_path)  
    
    return foldername

# deprecated: recursion style
""" # [directory_name]/[filename]_[filenum].csv
def create_savename(abs_dir, filename, filenum=1, new_folder=True):
    This function will create a proper filename for the output file
    if filenum == 1:
        filename = os.path.basename(filename).split(".")[0]
        foldername = "output_1"
        if new_folder:
            foldername = create_folder(abs_dir, foldername)
        filename = os.path.join(abs_dir,
                                foldername,
                                f"{filename}_{filenum}.csv")
    else:
        filename = re.sub("_(\d+)\.csv$", f"_{str(filenum)}.csv", filename)
    if not os.path.exists(filename):
        return filename
    else:
        return create_savename(abs_dir, filename, filenum + 1) """

"""
# [directory_name]/[filename]_[filenum].csv
def create_savename(abs_dir, filename, filenum=1, new_folder=True):
    # This function will create a proper filename for the output file 
    filename = os.path.basename(filename).split(".")[0]
    foldername = "output_1"
    if new_folder:
        foldername = create_folder(abs_dir, foldername)
    filename = os.path.join(abs_dir,
                            foldername,
                            f"{filename}_{filenum}.csv")
    while os.path.exists(filename):
        if filenum > 100:
            raise Exception("A bug in creating a filename!")
        filenum += 1
        filename = re.sub("_(\d+)\.csv$", f"_{str(filenum)}.csv", filename)
    
    return filename
"""

# [directory_name]/[filename].csv
def create_savename(abs_dir, filename, filenum=1, new_folder=True, no_create=False):
    """This function will create a proper filename for the output file"""   
    filename = os.path.basename(filename).split(".")[0]
    if no_create:
        foldername = "output"
        if not os.path.exists(os.path.join(abs_dir, foldername)):
            os.makedirs(foldername)
    else:    
        foldername = "output_1"
        if new_folder:
            foldername = create_folder(abs_dir, foldername)
    filename = os.path.join(abs_dir,
                            foldername,
                            f"{filename}.csv")
   
    return filename
