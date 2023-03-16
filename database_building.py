import argparse
import os

from src.database_building.add_id import add_id
from src.database_building.filter_database import filter_database
from src.database_building.filter_partial_sequence import filter_partial_sequence
from src.database_building.get_entry import get_entry


def parent_arguments():
    parent_parser = argparse.ArgumentParser(description="Parent parser.",
                                            add_help=False)
    parent_parser.add_argument("-i", "--input", type=str, required=True,
                               help="input path")
    parent_parser.add_argument("-o", "--output", type=str,
                               default=os.path.dirname(__file__),
                               help="output path")

    return parent_parser


def run_add_id(args):
    add_id_folder = os.path.join(os.path.normpath(args.output), "add_id")
    os.makedirs(add_id_folder, exist_ok=True)
    input_file = args.input
    basename = os.path.basename(input_file)
    enzyme_id = args.enzyme_id.replace("_", "~~~")
    line = add_id(input_file, enzyme_id)
    with open(os.path.join(add_id_folder, basename), "w") as f:
        f.writelines(["".join(entry) for entry in line])


def run_get_entry(args):
    get_entry_folder = os.path.join(os.path.normpath(args.output), "get_entry")
    os.makedirs(get_entry_folder, exist_ok=True)
    input_file = args.input
    basename = os.path.basename(input_file)
    line = get_entry(input_file)
    with open(os.path.join(get_entry_folder, basename), "w") as f:
        f.writelines(line)


def run_filter_database(args):
    filter_database_folder = os.path.join(os.path.normpath(args.output),
                                          "filter_database")
    os.makedirs(filter_database_folder, exist_ok=True)
    database = args.input
    entry_list = args.entry_list
    basename = os.path.basename(database)
    line = filter_database(entry_list, database)
    with open(os.path.join(filter_database_folder, basename), "w") as f:
        f.writelines(line)


def run_filter_partial(args):
    filter_partial_folder = os.path.join(os.path.normpath(args.output),
                                         "filter_partial")
    os.makedirs(filter_partial_folder, exist_ok=True)
    database = args.input
    basename = os.path.basename(database)
    sequences = filter_partial_sequence(database)
    with open(os.path.join(filter_partial_folder, basename), "w") as f:
        f.writelines(["".join(entry) for entry in sequences])


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help="module name")

    add_id_parser = subparser.add_parser(
        "add_id",
        parents=[parent_arguments()],
        help="add custom-built ID to entries")
    add_id_parser.add_argument(
        "enzyme_id", type=str,
        help="id that will be added to the entries")
    add_id_parser.set_defaults(func=run_add_id)

    get_entry_parser = subparser.add_parser(
        "get_entry",
        parents=[parent_arguments()],
        help="extract protein entry IDs from a database")
    get_entry_parser.set_defaults(func=run_get_entry)

    filter_database_parser = subparser.add_parser(
        "filter_database",
        parents=[parent_arguments()],
        help="eliminate custom entries from the orginal database")
    filter_database_parser.add_argument(
        "entry_list",
        help="entry list generated from get_entry")
    filter_database_parser.set_defaults(func=run_filter_database)

    filter_partial_parser = subparser.add_parser(
        "filter_partial",
        parents=[parent_arguments()],
        help="filter sequences labelled with PARTIAL")
    filter_partial_parser.set_defaults(func=run_filter_partial)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()
    args.func(args)
