import glob
import logging
import os
from shutil import rmtree
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Union

import tomli

# Package layout: ./src/biopathpred/modules/utils.py
# ROOT_DIR: the absolute path of ./
ROOT_DIR = Path(__file__).parents[3].resolve()

class Configuration():
    """Configure input and output path, and check parameters.

    Attributes:
        args: The given argparse `Namespace` object for storing command-line arguments.
        type: The name of the module or whole pipeline to be run.
        input_path: The input path for the module to be run.
        output_path: The output path for the module to be run.
        file_list: The file list for the files with the right extension in the input path.
        logger: A logger for storing the info from each module.
        thread_num: An integer of available cpu threads.
        default: Default configs for each module.
    """
    def __init__(self, args):
        """Initialize the instance based on argparse inputs.
        
        Args:
            args: Parsed arguments from `argparse`.
        """
        self.args = args
        self.type = args.type
        self.input_path = None
        self.output_path = None
        self._base_path = self._get_base_path()
        self.file_list = None
        self.logger = self._config_logging()
        self.thread_num = self._get_thread_num()
        self.default = self._load_default_config()

        self._file_ext_dict = {"prodigal": {"input": "fna", "output": "faa"},
                               "blast": {"input": "faa", "output": "xml"},
                               "parse_blast": {"input": "xml", "output": "csv"},
                               "best_blast": {"input": "csv", "output": "csv"},
                               "match_enzyme": {"input": "csv", "output": "txt"},
                               "mapping_analysis": {"input": "txt", "output": "csv"}}

    def check_io(self, module: Literal["prodigal", "blast", "parse_blast",
                                       "best_blast", "match_enzyme",
                                       "mapping_anaylsis"]):
        """Determine the input and output path for each module.

        This method will set the input and output path of the object,
        update the `type` attribute to the module calling this method,
        and load

        Args:
            type: The name of the module to be executed.
        """
        if self.type == module or self.type == "main":
            self.input_path = Path(self.args.input).resolve()
        else:
            # If the above condition is not satisfied, it means the input
            # will be from the last module.
            self.input_path = self.output_path

        self.output_path = self._base_path.joinpath(module)
        self.output_path.mkdir(exist_ok=True)
        self.type = module

        self.file_list = self._get_files_in_input_path()

        self._load_params()


    def _get_files_in_input_path(self):
        if self.input_path.is_dir():
            filetype = self._file_ext_dict[self.type]["input"]
            pattern = f"**/*.{filetype}"
            file_list = list(self.input_path.glob(pattern))
        elif self.input_path.is_file():
            file_list = [self.input_path]
        
        return file_list


    def _load_params(self):
        """Load the parameters from `config.toml`.
        
        Each module may have its own extra parameters. These parameters will be
        loaded from `config.toml` if not specified.
        """
        if self.type == "blast":
            self.database = self.args.database
            if self.database is None:
                database_path = self.default["database"]["path"]
            self.database = Path(database_path)
            self._check_blast_database(self.database)
        elif self.type == "best_blast":
            self.criteria = self.args.criteria
            if self.criteria is None:
                self.criteria = self.default["criteria"]["column"]
            self.filter = self.args.filter
            if self.filter is None:
                self.filter = self.default["criteria"]["filter"]
        elif self.type == "match_enzyme":
            self.model = self.args.model
            if self.model is None:
                self.model = self.default["match_enzyme"]["model"]


    def _get_base_path(self):
        """Determine the base output path.
        
        If the output path is specified by the user, it will be the base path;
        otherwise the output path will be the root directory of biopathpred
        package.
        """
        try:
            base_path = Path(self.args.output).resolve()
        except TypeError:
            # Raised when the user doesn't specify the output path.
            base_path = ROOT_DIR.joinpath("output")
        
        return base_path


    def create_savepath(self, filename):
        """Create the path for saving a file.
        
        The created path will be the output path appended by the given filename.

        Args:
            filename: A string of filename.
        
        Returns:
            A Path object for the file to save at.
        """
        filetype = self._file_ext_dict[self.type]["output"]
        basename_no_extension = Path(filename).stem
        savename_new_extension = self.output_path.joinpath(f"{basename_no_extension}.{filetype}")

        return savename_new_extension 


    def clean_module_outputs(self,
        module: Union[Literal["prodigal", "blast", "parse_blast", "best_blast"], List[str]]):
        """Remove the files generated from the module.

        Args:
            module: The module name.
        """
        if isinstance(module, str):
            to_be_removed = self._base_path.joinpath(module)
            rmtree(to_be_removed)
        elif isinstance(module, list):
            for single_module in module:
                to_be_removed = self._base_path.joinpath(single_module)
                rmtree(to_be_removed)


    def _config_logging(self):
        now = datetime.now().strftime("%y%m%d%H%M%S")
        logger = logging.getLogger("pipeline_log")
        logger.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s\t[%(levelname)s]\t%(message)s",
                                    "%Y-%m-%d %H:%M:%S")
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        try:
            logging_path = self._base_path.joinpath(f"log_{now}.txt")
            os.makedirs(self.args.output, exist_ok=True)
        except TypeError:
            logging_path = ROOT_DIR.joinpath(f"log_{now}.txt")

        fh = logging.FileHandler(logging_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger


    def _get_thread_num(self):
        """Determine the maximum number of processes to be created.
        
        If the user doesn't specify the number of threads by --cpus argument,
        all available threads in the computer will be used.
        """
        max_thread_num = int(os.cpu_count())
        thread_num = self.args.cpus
        if thread_num > max_thread_num or thread_num == 0:
            thread_num = max_thread_num
        
        self.logger.info(f"Use {thread_num} thread(s).")

        return thread_num


    def _load_default_config(self):
        config_path = ROOT_DIR.joinpath("config.toml")
        with open(config_path, "rb") as f:
            self.logger.info(f"Load configs from {config_path}")
            configs = tomli.load(f)
        
        return configs


    def _check_blast_database(self, database_path: Path):
        self.logger.info("Check blast database existence")
        if database_path.is_file():
            self.logger.info(f"Database: {database_path.name}")
        else:
            raise Exception("Blast database does not exist. Check config.toml before running.")
