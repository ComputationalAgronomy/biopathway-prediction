import os
import sys

if __name__ == "__main__":
    from util import *
else:
    from .util import *



abs_dir = os.path.dirname(__file__)
assert len(sys.argv) == 3, "Invalid arguments"
name = sys.argv[1]
filter_name = sys.argv[2]



def filter_fasta(filename, filter_list):
    """This function will filter out the custom-curated protein entries in database"""
    try:
        line = []
        with open(filename, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    read_line = read_line.strip("\n")
                    entry, _ = read_line.split(" ", 1)
                    _, entry_id, _ = entry.split("|")
                    if entry_id in filter_list:
                        continue
                    # newline and check if the last entry exists
                    try:
                        line[-1][1] += "\n"
                    except:
                        pass
                    line.append([read_line])
                    line[-1].append("")
                else:
                    try:
                        # merge fasta sequence
                        line[-1][1] += read_line
                    except IndexError:
                        print("Error in input format")
                        return
            return line
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")

if os.path.isfile(name):
    with open(filter_name, "r") as f:
        filter_list = [line.strip("\n") for line in f.readlines()]
    line = filter_fasta(name, filter_list)
    basename = os.path.basename(name)
    with open(os.path.join(abs_dir, "output_2", basename), "w") as f:
            # concatenate all the entries
            j = ["\n".join(i) for i in line]
            f.writelines(j)
else:
    print("File does not exist")
    sys.exit()