def split_fasta(file):
    """
    Split different protein entries in database.
    
    Return
    ------
    2d list: [[title_1, sequence_1], [title_2, sequence_2], ...]
    """
    try:
        line = []
        with open(file, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    line.append([read_line])
                    line[-1].append("")
                else:
                    try:
                        # merge fasta sequence
                        line[-1][1] += read_line
                    except IndexError:
                        print("Incorrect input format")
                        return
            return line
    except FileNotFoundError:
        print(f"Cannot find '{file}'")