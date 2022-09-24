def filter_fasta(filter, filename):
    """This function will filter out the custom-curated protein entries in database"""
    try:
        line = []
        with open(filter, "r") as f:
            filter_list = [line.strip("\n") for line in f.readlines()]
        with open(filename, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    find_new_entry = False
                    entry, _ = read_line.split(" ", 1)
                    _, entry_id, _ = entry.split("|")
                    if entry_id in filter_list:
                        find_new_entry = True
                        continue
                    line.append([read_line])
                    line[-1].append("")
                else:
                    if not find_new_entry:
                        try:
                            # merge fasta sequence
                            line[-1][1] += read_line
                        except IndexError:
                            print("Error in input format")
                            return
            return line
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")