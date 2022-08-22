import os

# path: [directory_name]/[filename]_[filenum].csv
def create_savename(abs_dir, filename, filenum=1):
    """This function will create a proper filename for the output file"""
    if filenum == 1:
        filename = os.path.basename(filename).split(".")[0]
    output_filename = os.path.join(abs_dir,
                            f"{filename}_{filenum}.csv")
    if not os.path.exists(output_filename):
        return output_filename
    else:
        return create_savename(abs_dir, filename, filenum + 1)
    
