import os
import sys
import re
import glob
from tqdm import tqdm

if __name__ == "__main__":
    from util import *
else:
    from .util import *

from Bio.Blast import NCBIXML


abs_dir = os.path.dirname(__file__)
assert len(sys.argv) == 2, "Invalid arguments"
name = sys.argv[1]

def parse_blast(filename, output_filename):
    try:
        with open(filename, "r") as result, \
            open(output_filename, "w") as output:
            blast_records = NCBIXML.parse(result)
            output.write("id,start,end,alignment_id,enzyme_id,enzyme_code," +
                         "product,organism,existence,gene,score,evalue," +
                         "identity_percentage,query_coverage\n")
            for blast_record in blast_records:
                # the output from prodigal is delimited by '#'
                query_list = [element.strip(" ") for element in blast_record.query.split("#")]
                id, start, end, strand, _ = query_list
                
                write_list = []
                for alignment in blast_record.alignments:
                    alignment_title = alignment.title
                    _, alignment_id, description = alignment_title.split(" ", 2)
                    _, alignment_id, _ = alignment_id.split("|")
                    element = re.search("(.*) OS=(.*) OX=.* PE=(\d)", description)
                    # OS: organism
                    organism = element.group(2)
                    # PE: protein existence
                    existence = element.group(3)
                    product = element.group(1).replace(",", "")
                    # if labeled: {enzyme_id}_{enzyme_code}_{product}
                    # if not    : {product}
                    product = product.split("_")
                    if len(product) == 1:
                        product = product[0]
                        enzyme_id = "-"
                        enzyme_code = "-"
                    elif len(product) == 3:
                        enzyme_id = product[0]
                        enzyme_code = product[1]
                        product = product[2]
                    else:
                        print("product parsing error")
                        sys.exit()
                    gene = re.search("GN=(.*) PE=", description)
                    if gene is None:
                        gene = "-"
                    else:
                        gene = gene.group(1)
                    alignment_info = f"{alignment_id},{enzyme_id},{enzyme_code}," \
                        f"{product},{organism},{existence},{gene}"
                    for hsp in alignment.hsps:
                        to_write = f"{id},{start},{end}," \
                          f"{alignment_info},{hsp.bits},{hsp.expect}," \
                          f"{round(hsp.identities / hsp.align_length * 100, 3)}," \
                          f"{round(100 * (hsp.align_length - hsp.gaps) / blast_record.query_length, 3)}\n"
                        write_list.append(to_write)
                output.writelines(write_list)
    except FileNotFoundError:
        print(f"Cannot find '{filename}'")
        sys.exit()


if os.path.isdir(name):
    # find fasta files in the directory
    file_list = glob.glob(os.path.join(name, "**/*.xml"), recursive=True)
    file_list = [file.replace("\\", "/") for file in file_list]
    new_folder = True
    for filename in tqdm(file_list):
        output = create_savename(abs_dir, filename,
                                   new_folder=new_folder)
        parse_blast(filename, output)
elif os.path.isfile(name):
    output = create_savename(abs_dir, name)
    parse_blast(name, output)
else:
    print("Invalid file or directory name")
    sys.exit()

