def add_id(line, enzyme_id):
    element = line.split(" ", 1)
    product_info = element[1]
    return f"{element[0]} {enzyme_id}~~~{product_info}"
    
def split_fasta(filename, enzyme_id):
    """This function will split different protein entries in database"""
    try:
        line = []
        with open(filename, "r") as f:
            for read_line in f.readlines():
                if read_line.startswith(">"):
                    read_line = add_id(read_line, enzyme_id)
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
