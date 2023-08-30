def get_entry(filename):
    """
    Extract protein entry IDs (eg. P32961, P46011) from a database

    Return
    ------
    A list with entry IDs (with line feed at the end of each ID)

    See also
    --------
    database_building.py
    """
    try:
        line = []
        for read_line in f.readlines():
            if read_line.startswith(">"):
                read_line = read_line.strip("\n")
                entry, _ = read_line.split(" ", 1)
                _, entry_id, _ = entry.split("|")
                line.append(f"{entry_id}\n")
        return line
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")
