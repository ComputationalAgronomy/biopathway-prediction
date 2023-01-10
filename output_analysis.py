import argparse
import os

from src.output_analysis.cytoscape_network_map import cytoscape_format_conversion
from src.output_analysis.enzyme_mapping_analysis import enzyme_mapping_analysis


def main():
    abs_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--cytoscape", help="[input_path]")
    parser.add_argument("--mapping_analysis", help="[input_path]")

    args = parser.parse_args()

    output_path = os.path.join(abs_dir, "analysis_output")
    os.makedirs(output_path, exist_ok=True)

    if args.cytoscape is not None:
        cytoscape_folder = os.path.join(output_path, "cytoscape")
        os.makedirs(cytoscape_folder, exist_ok=True)
        input_path = args.cytoscape
        cytoscape_format_conversion(input_path, cytoscape_folder)

    if args.mapping_analysis is not None:
        mapping_analysis_folder = os.path.join(output_path, "mapping_analysis")
        os.makedirs(mapping_analysis_folder, exist_ok=True)
        input_path = args.mapping_analysis
        enzyme_mapping_analysis(input_path, mapping_analysis_folder)


if __name__ == "__main__":
    main()
