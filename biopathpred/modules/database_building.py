import re
from collections import OrderedDict
from pathlib import Path

from Bio import SeqIO

REGEX_FRAGMENT = re.compile(r"\(Fragment\)")
REGEX_ENZYME_FILENAME = re.compile(r"^(\d+_\w+).fasta")


def build_blast_db(input_dir, output_filepath, filter_fragment=False):
    print("Collect fasta files with pattern: [int]_[str].fasta")
    input_path = Path(input_dir)
    output_path = Path(output_filepath)
    if output_path.is_file():
        output_path.unlink()
    total_entries = 0

    for filepath in input_path.glob("*.fasta"):
        search_result = REGEX_ENZYME_FILENAME.search(filepath.name)
        if search_result is None:
            continue
        enzyme_id_name = search_result.group(1)

        fasta_records = parse_fasta(filepath)

        if filter_fragment:
            fasta_records = filter_partial_sequence(fasta_records)

        fasta_records = add_id(fasta_records, enzyme_id_name)

        with open(output_filepath, "a") as f:
            SeqIO.write(fasta_records, f, "fasta")

        print(f"{filepath.name}: {len(fasta_records)} entries")
        total_entries += len(fasta_records)

    print(f"Collect {total_entries} entries")


def parse_fasta(filepath):
    return list(SeqIO.parse(filepath, "fasta"))


def add_id(fasta_records: OrderedDict, enzyme_id_name: str) -> str:
    """Add custom-built ID to entries.
    Examples:
        Format: [number]_[enzyme_name] (eg. 1_iam1, 2_iaa)

        Original Uniprot version of sequence:
        >sp|O49342|C71AD_ARATH SEQ_1
        AAAAAA

        Processed sequence:
        >sp|O49342|C71AD_ARATH 1~~~iam1~~~SEQ_1
        AAAAAA
    """
    enzyme_id_name = enzyme_id_name.replace("_", "~~~", 1)
    for record in fasta_records:
        record_id, record_info = record.description.split(" ", 1)
        record.description = f"{record_id} {enzyme_id_name}~~~{record_info}"

    return fasta_records


def filter_database(fasta_records, database_records: dict):
    fasta_dict = {record.id: record for record in fasta_records}
    database_dict = {record.id: record for record in database_records}
    records_to_remove = []
    for target_id in fasta_dict.keys():
        if target_id in database_dict:
            records_to_remove.append(database_dict[target_id])

    for record in records_to_remove:
        database_records.remove(record)

    return database_records


def filter_partial_sequence(fasta_records):
    filterd_records = [
        record for record in fasta_records if REGEX_FRAGMENT.search(record.description) is None]

    return filterd_records
