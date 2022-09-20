import os
import sys
import subprocess

def run_prodigal(input_path, output_path):
    abs_path = os.path.dirname(__file__)
    prodigal_script = os.path.join(abs_path, "run_prodigal.sh")
    try:
        subprocess.run(["bash", prodigal_script, input_path, output_path])
    except Exception:
        print("prodigal running error!")
        sys.exit()

def run_blast(input_path, output_path):
    abs_path = os.path.dirname(__file__)
    blast_script = os.path.join(abs_path, "run_blast.sh")
    try:
        subprocess.run(["bash", blast_script, input_path, output_path])
    except Exception:
        print("blastp running error!")
        sys.exit()
