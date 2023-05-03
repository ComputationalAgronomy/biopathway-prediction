import os
import subprocess
import sys


def run_prodigal(config):
    config.check_io(type="prodigal")
    abs_path = os.path.dirname(__file__)
    prodigal_script = os.path.join(abs_path, "run_prodigal.sh")
    config.logger.info("Start prodigal gene prediction")
    prodigal_output = subprocess.run(["bash", prodigal_script,
                                      config.input_path, config.output_path,
                                      str(config.thread_num)],
                                     capture_output=False)
    if prodigal_output.returncode == 3:
        config.logger.error("Invalid prodigal input!")
        sys.exit()
    if prodigal_output.returncode != 0:
        config.logger.error("prodigal runtime error!")
        sys.exit()
    config.logger.info("Finish prodigal gene prediction")


def run_blast(config):
    config.check_io(type="blast")
    abs_path = os.path.dirname(__file__)
    blast_script = os.path.join(abs_path, "run_blast.sh")
    config.logger.info("Finish blastp alignment")
    blast_output = subprocess.run(["bash", blast_script, config.input_path,
                                   config.output_path, config.database,
                                   config.thread_num], capture_output=False)
    if blast_output.returncode == 3:
        config.logger.error("Invalid blastp input!")
        sys.exit()
    elif blast_output.returncode != 0:
        config.logger.error("blastp runtime error!")
        sys.exit()
