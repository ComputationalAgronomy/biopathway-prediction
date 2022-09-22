import os
import sys

abs_dir = os.path.dirname(__file__)
assert len(sys.argv) == 2, "Invalid arguments"
name = sys.argv[1]

def find_entry(filename):
    try:
        line = []
        with open(filename, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    read_line = read_line.strip("\n")
                    entry, _ = read_line.split(" ", 1)
                    _, entry_id, _ = entry.split("|")
                    line.append(f"{entry_id}\n")
            return line
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")

if os.path.isfile(name):
    line = find_entry(name)
    basename = os.path.basename(name)
    with open(os.path.join(abs_dir, "output_1", basename), "w") as f:
            # concatenate all the entries
            f.writelines(line)
else:
    print("File does not exist")
    sys.exit()