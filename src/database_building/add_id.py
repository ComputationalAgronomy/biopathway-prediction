from .database_utils import split_fasta


def add_id(file, enzyme_id):
    entries = split_fasta(file)
    entry_title = [entry[0] for entry in entries]
    entry_id, product_info = entry_title.split(" ", 1)
    return f"{entry_id} {enzyme_id}~~~{product_info}"
