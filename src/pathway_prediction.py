import argparse
import multiprocessing as mp
import subprocess
import sys
import time
from functools import partial
from math import ceil
from pathlib import Path
from typing import Literal

from tqdm import tqdm

from biopathpred.modules.best_blast import find_best_blast
from biopathpred.modules.match_enzyme import start_match_enzyme
from biopathpred.modules.parse_blastp_xml import parse_blast
from biopathpred.modules.utils import Configuration


# Run whole pipeline
def main(config: Configuration):
    time_start = time.perf_counter()

    run_prodigal(config)
    run_blast(config)
    run_parse_blast(config)
    run_find_best_blast(config)
    run_match_enzyme(config)

    time_end = time.perf_counter()
    config.logger.info(f"Elapsed time: {round(time_end - time_start, 2)}sec")


# Run individual module
def run_prodigal(config: Configuration):
    """Call the executable to run progidal gene prediction."""
    config.check_io(module="prodigal")
    prodigal_executable = Path(config.default["executable"]["prodigal_path"]).resolve()
    config.logger.info("Start prodigal gene prediction")

    if config.thread_num != 1:
        with mp.Pool(config.thread_num) as p:
            # https://stackoverflow.com/questions/32515389/does-multiprocessing-pool-imap-has-a-variant-like-starmap-that-allows-for-mult
            # https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar
            list(
                tqdm(
                    p.imap(partial(single_job_prodigal, prodigal_executable=prodigal_executable, config=config),
                        config.file_list,
                        chunksize=10),
                    total=len(config.file_list)
                    )
                )
    else:
        for file in tqdm(config.file_list):
            single_job_prodigal(file, prodigal_executable, config)

    config.logger.info("Finish prodigal gene prediction")


def single_job_prodigal(file, prodigal_executable, config: Configuration):
    savepath = config.create_savepath(file)
    prodigal_output = subprocess.run([prodigal_executable,
                                        "-i", file,
                                        "-a", savepath],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT,
                                        capture_output=False)
    
    if prodigal_output.returncode != 0:
        config.logger.error("prodigal runtime error!")
        sys.exit()


def run_blast(config: Configuration):
    """Call the executable to run blastp alignment."""
    config.check_io(module="blast")
    blast_executable = Path(config.default["executable"]["diamond_path"])
    config.logger.info("Start blastp alignment")

    if config.thread_num != 1:
        # Diamond already adopts multithreading, so use less threads here
        with mp.Pool(ceil(config.thread_num / 4)) as p:
            list(
                tqdm(
                    p.imap(partial(single_job_blast, blast_executable=blast_executable, config=config),
                        config.file_list,
                        chunksize=10),
                    total=len(config.file_list)
                    )
                )
    else:
        for file in tqdm(config.file_list):
            single_job_blast(file, blast_executable, config)

    config.logger.info("Finish blastp alignment")


def single_job_blast(file, blast_executable, config: Configuration):
    savepath = config.create_savepath(file)
    blast_output = subprocess.run([blast_executable,
                                    "blastp",
                                    "-d", config.database,
                                    "-q", file,
                                    "-o", savepath,
                                    "--outfmt", "5",
                                    "--xml-blord-format"],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.STDOUT,
                                    capture_output=False)

    if blast_output.returncode != 0:
        config.logger.error("blastp runtime error!")
        sys.exit()


def run_parse_blast(config: Configuration):
    """Run parse_blastp_xml module to parse the blastp result."""
    config.check_io(module="parse_blast")
    config.logger.info("Parse blastp result")

    if config.thread_num != 1:
        with mp.Pool(config.thread_num) as p:
            list(
                tqdm(
                    p.imap(partial(single_job_module, module=parse_blast, config=config),
                        config.file_list,
                        chunksize=10),
                    total=len(config.file_list)
                    )
                )
    else:
        for file in tqdm(config.file_list):
            savepath = config.create_savepath(file)
            parse_blast(filepath=file, output_filepath=savepath)

    config.logger.info("Done!")


def single_job_module(file, module, config: Configuration):
    savepath = config.create_savepath(file)
    module(filepath=file, output_filepath=savepath)


def run_find_best_blast(config: Configuration):
    """Run the best_blast module to get the best blastp result of each alignment hit."""
    config.check_io(module="best_blast")
    config.logger.info("Select the best blastp result based on the configuration")
    
    if config.thread_num != 1:
        with mp.Pool(config.thread_num) as p:
            list(
                tqdm(
                    p.imap(partial(single_job_module, module=partial(find_best_blast, criteria=config.criteria, filter=config.filter), config=config),
                        config.file_list,
                        chunksize=10),
                    total=len(config.file_list)
                    )
                )
    else:
        for file in tqdm(config.file_list):
            savepath = config.create_savepath(file)
            find_best_blast(filepath=file, output_filepath=savepath,
                            criteria=config.criteria, filter=config.filter)
    
    config.logger.info("Done!")


def run_match_enzyme(config: Configuration):
    """Run the match_enzyme module to map the best alignment hit to the pathway of interest."""
    config.check_io("match_enzyme")
    config.logger.info("Match the best blastp result to the pathway")

    if config.thread_num != 1:
        with mp.Pool(config.thread_num) as p:
            list(
                tqdm(
                    p.imap(partial(single_job_module, module=partial(start_match_enzyme, model=config.model, verbose=config.args.verbose), config=config),
                        config.file_list,
                        chunksize=10),
                    total=len(config.file_list)
                    )
                )
    else:
        for file in tqdm(config.file_list):
            savepath = config.create_savepath(file)
            start_match_enzyme(filepath=file, output_filepath=savepath,
                            model=config.model, verbose=config.args.verbose)

    config.logger.info("Done!")


def parse_arguments():
    parser = argparse.ArgumentParser(parents=[parent_arguments(),
                                              optional_arguments()],
                                     conflict_handler="resolve")
    parser.set_defaults(func=main, type="main")

    # With subcommand: run individual module
    subparser = parser.add_subparsers(help="module name")
    prodigal_parser = subparser.add_parser(
        "prodigal",
        parents=[parent_arguments(), optional_arguments(case="prodigal")],
        conflict_handler="resolve")
    prodigal_parser.set_defaults(func=run_prodigal, type="prodigal")

    blast_parser = subparser.add_parser(
        "blastp",
        parents=[parent_arguments(), optional_arguments(case="blast")],
        conflict_handler="resolve")
    blast_parser.set_defaults(func=run_blast, type="blast")

    xml_parser = subparser.add_parser(
        "parse_xml",
        parents=[parent_arguments(), optional_arguments(case="parse_xml")],
        conflict_handler="resolve")
    xml_parser.set_defaults(func=run_parse_blast, type="parse_blast")

    best_blast_parser = subparser.add_parser(
        "best_blast",
        parents=[parent_arguments(), optional_arguments(case="best_blast")],
        conflict_handler="resolve")
    best_blast_parser.set_defaults(func=run_find_best_blast, type="best_blast")

    match_enzyme_parser = subparser.add_parser(
        "match_enzyme",
        parents=[parent_arguments(), optional_arguments(case="match_enzyme")],
        conflict_handler="resolve")
    match_enzyme_parser.set_defaults(
        func=run_match_enzyme, type="match_enzyme")

    args = parser.parse_args()

    return args


def parent_arguments():
    parent_parser = argparse.ArgumentParser(description="Parent parser.",
                                            add_help=False)
    parent_parser.add_argument("-i", "--input", type=str, required=True,
                               help="input a file or directory path")
    parent_parser.add_argument("-o", "--output", type=str, help="output path")
    parent_parser.add_argument("--cpus", type=int, default=0,
                               help="threads to be used (default: 0 (all available threads))")

    return parent_parser


def optional_arguments(case: Literal["main", "blast", "best_blast", "match_enzyme"] = "main"):
    optional_parser = argparse.ArgumentParser(description="Optional parser.",
                                              add_help=False)
    if case == "main":
        optional_parser.add_argument("-i", "--input", type=str, required=False,
                                     help="input a file or directory path")
        optional_parser.add_argument(
            "-d", "--database", type=str, help="database path")
        optional_parser.add_argument(
            "-c", "--criteria", type=str, help="selection criteria")
        optional_parser.add_argument(
            "-f", "--filter", nargs="*", type=str, help="filter options")
        optional_parser.add_argument(
            "-m", "--model", type=str, help="model name")
        optional_parser.add_argument("--verbose", action="store_true",
                                     help="print match_enzyme result to screen")
        # --debug not yet implemented
        optional_parser.add_argument("--debug", action="store_true",
                                     help="keep tmp folder if specified")
    elif case == "blast":
        optional_parser.add_argument(
            "-d", "--database", type=str, help="database path")
    elif case == "best_blast":
        optional_parser.add_argument(
            "-c", "--criteria", type=str, help="selection criteria")
        optional_parser.add_argument(
            "-f", "--filter", nargs="*", type=str, help="filter options")
    elif case == "match_enzyme":
        optional_parser.add_argument("param_start", type=int)
        optional_parser.add_argument("param_end", type=int)
        optional_parser.add_argument(
            "-m", "--model", type=str, help="model name")
        optional_parser.add_argument("--verbose", action="store_true",
                                     help="print match_enzyme result to screen")
    else:
        pass

    return optional_parser


if __name__ == "__main__":
    args = parse_arguments()
    config = Configuration(args)
    args.func(config)


