from logging import Filterer
import os
import argparse
from src.database_building.add_id import split_fasta
from src.database_building.filter_database import filter_fasta
from src.database_building.get_entry import get_entry
from src.util import make_dir

def main():
    abs_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--add_id", nargs=2, help="[input_file] [enzyme_id]")
    parser.add_argument("--get_entry", nargs=1, help="[input_file]")
    parser.add_argument("--filter_database", nargs=2, help="[entry_list] [database]")
    args = parser.parse_args()

    output_path = os.path.join(abs_dir, "database_output")
    make_dir(output_path)
    
    if args.add_id is not None:
        add_id_folder = os.path.join(output_path, "add_id")
        make_dir(add_id_folder)
        basename = os.path.basename(args.add_id[0])
        enzyme_id = args.add_id[1].replace("_", "~~~")
        line = split_fasta(args.add_id[0], enzyme_id)
        with open(os.path.join(add_id_folder, basename), "w") as f:
            f.writelines(line)
    
    if args.get_entry is not None:
        get_entry_folder = os.path.join(output_path, "get_entry")
        make_dir(get_entry_folder)
        basename = os.path.basename(args.get_entry[0])
        line = get_entry(args.get_entry[0])
        with open(os.path.join(get_entry_folder, basename), "w") as f:
            f.writelines(line)
    
    if args.filter_database is not None:
        filter_database_folder = os.path.join(output_path, "filter_database")
        make_dir(filter_database_folder)
        basename = os.path.basename(args.filter_database[1])
        line = filter_fasta(args.filter_database[0], args.filter_database[1])
        with open(os.path.join(filter_database_folder, basename), "w") as f:
            f.writelines(line)

if __name__ == "__main__":
    main()
