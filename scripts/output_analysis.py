import argparse
import os

from biopathpred.output_analysis.cytoscape_network_map import cytoscape_format_conversion
from biopathpred.output_analysis.enzyme_mapping_analysis import enzyme_mapping_analysis


def parent_arguments():
    parent_parser = argparse.ArgumentParser(description="Parent parser.",
                                            add_help=False)
    parent_parser.add_argument("-i", "--input", type=str, required=True,
                               help="input path")
    parent_parser.add_argument("-o", "--output", type=str,
                               default=os.path.dirname(__file__),
                               help="output path")

    return parent_parser


def run_func(args):
    output_folder = os.path.join(os.path.normpath(args.output), args.type)
    os.makedirs(output_folder, exist_ok=True)
    if args.type == "cytoscape":
        cytoscape_format_conversion(args.input, output_folder)
    elif args.type == "mapping_analysis":
        enzyme_mapping_analysis(args.input, output_folder)
    else:
        raise Exception("Unexpected Error!")


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help="module name")

    cytoscape_parser = subparser.add_parser(
        "cytoscape",
        parents=[parent_arguments()],
        help="convert the result to cytoscape-readable format"
    )
    cytoscape_parser.set_defaults(func=run_func, type="cytoscape")

    mapping_analysis_parser = subparser.add_parser(
        "mapping_analysis",
        parents=[parent_arguments()],
        help="analyze and summarize match_enzyme result"
    )
    mapping_analysis_parser.set_defaults(func=run_func, type="mapping_analysis")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()
    args.func(args)
