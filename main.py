import os
import sys
import subprocess
import argparse
from src.run_scripts import run_blast, run_prodigal

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input a file or directory path")
    args = parser.parse_args()
    abs_dir = os.path.dirname(__file__)
    run_prodigal(args.file, os.path.join(abs_dir, "tmp/prokka"))
    run_blast(os.path.join(abs_dir, "tmp/prokka"),
              os.path.join(abs_dir, "tmp/blast"))
