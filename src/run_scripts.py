import os
import sys
import subprocess

def run_prodigal(input_path, output_path):
    abs_path = os.path.dirname(__file__)
    prodigal_script = os.path.join(abs_path, "run_prodigal.sh")
    prodigal_output = subprocess.run(["bash", prodigal_script,
                                      input_path, output_path],
                                      capture_output=False)
    if prodigal_output.returncode != 0:
        print("prodigal running error!")
        sys.exit()

def run_blast(input_path, output_path, database_path, cpus):
    abs_path = os.path.dirname(__file__)
    blast_script = os.path.join(abs_path, "run_blast.sh")
    blast_output = subprocess.run(["bash", blast_script, input_path,
                                   output_path, database_path, cpus],
                                   capture_output=False)
    if blast_output.returncode != 0:
        print("blastp running error!")
        sys.exit()

def cpu_num():
    res = subprocess.run("grep -c ^processor /proc/cpuinfo", shell=True,
                          stdout=subprocess.PIPE)
    return int(res.stdout)     
