import argparse
import multiprocessing as mp
import subprocess
import time
from functools import partial
from pathlib import Path
from typing import Literal

from tqdm import tqdm

from biopathpred.modules.best_blast import find_best_blast
from biopathpred.modules.configuration import Configuration
from biopathpred.modules.database_building import build_blast_db
from biopathpred.modules.match_enzyme import start_match_enzyme
from biopathpred.modules.parse_blastp_xml import parse_blast
from biopathpred.modules.result_summary import result_summary


# Run whole pipeline
def pipeline(config: Configuration):
    time_start = time.perf_counter()

    run_prodigal(config)
    run_blast(config)
    run_parse_blast(config)
    run_find_best_blast(config)
    run_match_enzyme(config)
    run_result_summary(config)

    if not config.args.debug:
        config.clean_module_outputs(module=["prodigal", "blast", "parse_blast",
                                            "best_blast"])

    time_end = time.perf_counter()
    config.logger.info(f"Elapsed time: {round(time_end - time_start, 2)}sec")


def multiprocess_dispatch(config: Configuration, func, thread_num=None, **kwargs):
    thread_num = thread_num if thread_num is not None else config.thread_num
    with mp.Pool(thread_num) as p:
        # https://stackoverflow.com/questions/32515389/does-multiprocessing-pool-imap-has-a-variant-like-starmap-that-allows-for-mult
        # https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar
        list(
            tqdm(
                p.imap(partial(func, config=config, **kwargs),
                       config.file_list,
                       chunksize=10),
                total=len(config.file_list)
            )
        )


# Run individual module
def run_prodigal(config: Configuration):
    """Call the executable to run progidal gene prediction."""
    config.check_io(module="prodigal")
    prodigal_executable = Path(config.default["executable"]["prodigal_path"]).resolve()
    config.logger.info("Start prodigal gene prediction")

    if config.thread_num != 1:
        multiprocess_dispatch(config, single_job_executable,
                              module="prodigal",
                              executable=prodigal_executable)
    else:
        for file in tqdm(config.file_list):
            single_job_executable(file, "prodigal", prodigal_executable, config)

    config.logger.info("Finish prodigal gene prediction")


def run_blast(config: Configuration):
    """Call the executable to run blastp alignment."""
    config.check_io(module="blast")
    blast_executable = Path(config.default["executable"]["diamond_path"])
    config.logger.info("Start blastp alignment")

    if config.thread_num != 1:
        # Diamond already adopts multithreading, so use less threads here
        multiprocess_dispatch(config, single_job_executable,
                              module="blast",
                              thread_num=config.thread_num // 2,
                              executable=blast_executable)
    else:
        for file in tqdm(config.file_list):
            single_job_executable(file, "blast", blast_executable, config)

    config.logger.info("Finish blastp alignment")


def single_job_executable(file, module, executable, config: Configuration):
    savepath = config.create_savepath(file)

    if module == "prodigal":
        output = subprocess.run([executable,
                                 "-i", file,
                                 "-a", savepath],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE,
                                text=True)
    elif module == "blast":
        output = subprocess.run([executable,
                                 "blastp",
                                 "-d", config.database,
                                 "-q", file,
                                 "-o", savepath,
                                 "--outfmt", "5",
                                 "--xml-blord-format"],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE,
                                text=True)

    if output.returncode != 0:
        # Diamond will raise an error if the input file is empty
        msg = "Error: Error detecting input file format. First line seems to be blank."
        if not output.stderr.strip().endswith(msg):
            print(output.stderr)
            config.logger.error(f"{module} runtime error!")
            raise SystemExit


def run_parse_blast(config: Configuration):
    """Run parse_blastp_xml module to parse the blastp result."""
    config.check_io(module="parse_blast")
    config.logger.info("Parse blastp result")

    if config.thread_num != 1:
        multiprocess_dispatch(config, single_job_module,
                              module=parse_blast)
    else:
        for file in tqdm(config.file_list):
            savepath = config.create_savepath(file)
            parse_blast(filepath=file, output_filepath=savepath)


def run_find_best_blast(config: Configuration):
    """Run the best_blast module to get the best blastp result of each alignment hit."""
    config.check_io(module="best_blast")
    config.logger.info("Select the best blastp result based on the configuration")

    if config.thread_num != 1:
        multiprocess_dispatch(config, single_job_module,
                              module=partial(
                                  find_best_blast,
                                  criteria=config.criteria,
                                  filter=config.filter
                              ))
    else:
        for file in tqdm(config.file_list):
            savepath = config.create_savepath(file)
            find_best_blast(filepath=file, output_filepath=savepath,
                            criteria=config.criteria, filter=config.filter)


def run_match_enzyme(config: Configuration):
    """Run the match_enzyme module to map the best alignment hit to the pathway of interest."""
    config.check_io(module="match_enzyme")
    config.logger.info("Match the best blastp result to the pathway")

    if config.thread_num != 1:
        multiprocess_dispatch(config, single_job_module,
                              module=partial(
                                  start_match_enzyme,
                                  model=config.model,
                                  verbose=config.args.verbose
                              ))
    else:
        for file in tqdm(config.file_list):
            savepath = config.create_savepath(file)
            start_match_enzyme(filepath=file, output_filepath=savepath,
                               model=config.model, verbose=config.args.verbose)


def single_job_module(file, module, config: Configuration):
    savepath = config.create_savepath(file)
    module(filepath=file, output_filepath=savepath)


def run_result_summary(config: Configuration):
    """Parse the result from match_enzyme module"""
    config.check_io(module="result_summary")
    config.logger.info("Parse the prediction result")
    result_summary(path=config.input_path, output_path=config.output_path)


def parse_arguments():
    parser = argparse.ArgumentParser(parents=[parent_arguments(),
                                              optional_arguments()],
                                     conflict_handler="resolve")
    parser.set_defaults(func=pipeline, type="main")

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

    result_summary_parser = subparser.add_parser(
        "result_summary",
        parents=[parent_arguments(), optional_arguments(case="result_summary")],
        conflict_handler="resolve")
    result_summary_parser.set_defaults(
        func=run_result_summary, type="result_summary")

    build_db_parser = subparser.add_parser(
        "build_db",
        parents=[parent_arguments(), optional_arguments(case="build_db")],
        conflict_handler="resolve")
    build_db_parser.set_defaults(
        func=build_blast_db, type="build_db")

    args = parser.parse_args()

    return args


def parent_arguments():
    parent_parser = argparse.ArgumentParser(description="Parent parser.",
                                            add_help=False)
    parent_parser.add_argument("-i", "--input", type=str, required=True,
                               help="input a file or directory path")
    parent_parser.add_argument("-o", "--output", type=str, help="output path")
    parent_parser.add_argument("--cpus", type=int, default=0,
                               help="number of processes to be created (default: available_threads / 2)")

    return parent_parser


def optional_arguments(case: Literal["main", "prodigal", "blast",
                                     "parse_blast", "best_blast",
                                     "match_enzyme", "result_summary",
                                     "build_db"] = "main"):
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
        optional_parser.add_argument("--debug", action="store_true",
                                     help="keep all intermediate files if specified")
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
    elif case == "build_db":
        optional_parser.add_argument("--no_fragment", action="store_true",
                                     help="do not keep fragment sequences")
    else:
        pass

    return optional_parser


def main():
    args = parse_arguments()

    if args.type != "build_db":
        config = Configuration(args)
        args.func(config)
    else:
        args.func(args.input, args.output)


if __name__ == "__main__":
    main()
