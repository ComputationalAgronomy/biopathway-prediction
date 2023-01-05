import argparse
import os
from logging import Filterer

from src.database_building.add_id import add_id
from src.database_building.filter_database import filter_fasta
from src.database_building.get_entry import get_entry
from src.database_building.filter_partial_sequence import filter_partial_sequence


def main():
    abs_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--add_id", nargs=2, help="[input_file] [enzyme_id]")
    parser.add_argument("--get_entry", nargs=1, help="[input_file]")
    parser.add_argument("--filter_database", nargs=2,
                        help="[entry_list] [database]")
    parser.add_argument("--filter_partial", nargs=1, help="[database]")
    args = parser.parse_args()

    output_path = os.path.join(abs_dir, "database_output")
    os.makedirs(output_path, exist_ok=True)

    if args.add_id is not None:
        add_id_folder = os.path.join(output_path, "add_id")
        os.makedirs(add_id_folder, exist_ok=True)
        input_file = args.add_id[0]
        basename = os.path.basename(input_file)
        enzyme_id = args.add_id[1].replace("_", "~~~")
        line = add_id(input_file, enzyme_id)
        with open(os.path.join(add_id_folder, basename), "w") as f:
            f.writelines(["".join(entry) for entry in line])

    if args.get_entry is not None:
        get_entry_folder = os.path.join(output_path, "get_entry")
        os.makedirs(get_entry_folder, exist_ok=True)
        input_file = args.get_entry[0]
        basename = os.path.basename(input_file)
        line = get_entry(input_file)
        with open(os.path.join(get_entry_folder, basename), "w") as f:
            f.writelines(line)

    if args.filter_database is not None:
        filter_database_folder = os.path.join(output_path, "filter_database")
        os.makedirs(filter_database_folder, exist_ok=True)
        entry_list, database = args.filter_database
        basename = os.path.basename(database)
        line = filter_fasta(entry_list, database)
        with open(os.path.join(filter_database_folder, basename), "w") as f:
            f.writelines(line)

    if args.filter_partial is not None:
        filter_partial_folder = os.path.join(output_path, "filter_partial")
        os.makedirs(filter_partial_folder, exist_ok=True)
        database = args.filter_partial[0]
        basename = os.path.basename(database)
        sequences = filter_partial_sequence(database)
        with open(os.path.join(filter_partial_folder, basename), "w") as f:
            f.writelines(["".join(entry) for entry in sequences])


if __name__ == "__main__":
    main()
