import os
import sys
import subprocess

def run_prodigal(config):
    config.check_io(type="prodigal")
    abs_path = os.path.dirname(__file__)
    prodigal_script = os.path.join(abs_path, "run_prodigal.sh")
    prodigal_output = subprocess.run(["bash", prodigal_script,
                                      config.input_path, config.output_path,
                                      str(config.thread_num)],
                                      capture_output=False)
    if prodigal_output.returncode != 0:
        print("prodigal runtime error!")
        sys.exit()

def run_blast(config):
    config.check_io(type="blast")
    abs_path = os.path.dirname(__file__)
    blast_script = os.path.join(abs_path, "run_blast.sh")
    blast_output = subprocess.run(["bash", blast_script, config.input_path,
                                   config.output_path, config.database,
                                   config.thread_num], capture_output=False)
    if blast_output.returncode != 0:
        print("blastp runtime error!")
        sys.exit()

 
