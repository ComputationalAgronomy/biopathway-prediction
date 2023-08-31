import re
import sys
import os
from Bio.Blast import NCBIXML


# csv column title
HEADER_ELEMENT = ["id", "start", "end", "alignment_id", "enzyme_id",
                  "enzyme_code",  "product", "organism", "existence", "gene", "score",
                  "evalue", "identity", "coverage"]
HEADER = ",".join(HEADER_ELEMENT) + "\n"

# FASTA headers
# See https://www.uniprot.org/help/fasta-headers
# OS: organism
# OX: organism identifier
# PE: protein existence
REGEX_ELEMENTS = re.compile("(.*) OS=(.*) OX=.* PE=(\\d)")

REGEX_PRODUCT = re.compile("^(.+)~{3}(.+)~{3}(.+)$")
REGEX_GENE = re.compile("GN=(.*) PE=")


def parse_product_split(labels):
    # if labeled: {enzyme_id}~~~{enzyme_code}~~~{product}
    # if not    : {product}
    labels_split = labels.replace(",", "").split("~~~")
    # Assuming only 3 parts or others
    try:
        enzyme_id, enzyme_code, product_name = labels_split[0:4]
    except ValueError:
        enzyme_id, enzyme_code, product_name = None, None, labels_split[0]
    return enzyme_id, enzyme_code, product_name


def parse_product_regex(labels):
    # if labeled: {enzyme_id}~~~{enzyme_code}~~~{product}
    # if not    : {product}
    match = REGEX_PRODUCT.search(labels)
    try:
        enzyme_id, enzyme_code, product_name = match.groups()
    except AttributeError:
        if not "~~~" in labels:
            enzyme_id, enzyme_code, product_name = None, None, labels
        else:
            raise ValueError("Invalid database product format")
    product_name = product_name.replace(",", " ")
    return enzyme_id, enzyme_code, product_name


def parse_gene(desc):
    gene = REGEX_GENE.search(desc)
    if gene is not None:
        gene = gene.group(1).replace(",", " ")
    else:
        gene = "-"
    return gene


def parse_alignment_title(alignment_title):
    alignment_id_full, description = alignment_title.split(" ", 2)[1:3]

    alignment_id = alignment_id_full.split("|")[1]
    element = REGEX_ELEMENTS.search(description)
    labels, organism, existence = element.groups()

    # deprecated
    # enzyme_id, enzyme_code, product_name = parse_product_split(labels)
    enzyme_id, enzyme_code, product_name = parse_product_regex(labels)

    gene = parse_gene(description)

    output_list = [alignment_id, enzyme_id, enzyme_code, product_name,
                   organism, existence, gene]
    output_str = ["" if i is None else i for i in output_list]
    alignment_info = ",".join(output_str)

    return alignment_info


def parse_blast(filepath, output_filepath):
    """
    Parse the results from diamond blastp that are in xml formats
    """
    try:
        with open(filepath, "r") as result, \
                open(output_filepath, "w") as output:
            blast_records = NCBIXML.parse(result)
            output.write(HEADER)
            try:
                for blast_record in blast_records:
                    # the output from prodigal is delimited by '#'
                    query_list = [element.strip(
                        " ") for element in blast_record.query.split("#")]
                    id, start, end, strand, _ = query_list
                    write_list = []
                    for alignment in blast_record.alignments:
                        alignment_info = parse_alignment_title(alignment.title)
                        for hsp in alignment.hsps:
                            evalue = hsp.bits
                            alignment_score = hsp.expect
                            identity = round(hsp.identities / hsp.align_length * 100, 3)
                            coverage = round(100 * (hsp.align_length - hsp.gaps) / blast_record.query_length, 3)
                            to_write = f"{id},{start},{end}," \
                                f"{alignment_info},{evalue},{alignment_score}," \
                                f"{identity},{coverage}\n"
                            write_list.append(to_write)
                    output.writelines(write_list)
            except ValueError:
                print(f"Find empty XML file: {os.path.basename(filepath)}")
    except FileNotFoundError:
        print(f"Cannot find '{filepath}'")
        sys.exit()
