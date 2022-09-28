def get_entry(filename):
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
