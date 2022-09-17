import os
import sys
import subprocess

abs_path = os.path.dirname(__file__)

def print_abs():
    print(os.path.dirname(__file__))

def run_prodigal(filename):
    abs_path = os.path.dirname(__file__)
    prodigal_script = os.path.join(abs_path, "run_prodigal.sh")
    try:
        subprocess.run(["bash", prodigal_script, filename])
    except Exception:
        print("prodigal running error!")
        sys.exit()

def run_blast(filename):
    abs_path = os.path.dirname(__file__)
    blast_script = os.path.join(abs_path, "run_blast.sh")
    try:
        subprocess.run(["bash", blast_script, filename])
    except Exception:
        print("blastp running error!")
        sys.exit()
