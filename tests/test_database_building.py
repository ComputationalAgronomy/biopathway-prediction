from pathlib import Path

import pytest

from biopathpred.modules.database_building import build_blast_db, parse_fasta

DATA_DIR = Path("tests/test_data/build_db")


@pytest.fixture(scope="session")
def expected_database():
    yield {"with_fragment": DATA_DIR / "expected/database.fasta",
           "no_fragment": DATA_DIR / "expected/database_no_fragment.fasta"}


@pytest.fixture(scope="session")
def seq_paths():
    yield {"seq_dir": DATA_DIR / "test_data",
           "seq1": DATA_DIR / "test_data/1_seq1.fasta",
           "seq2": DATA_DIR / "test_data/2_seq2.fasta"}


def test_parse_fasta(seq_paths):
    fasta_records = parse_fasta(seq_paths["seq2"])
    record = fasta_records[0]
    result = (record.id, record.description, str(record.seq))
    expected = ("sp|Q09109|TR2M_AGRRH",
                "sp|Q09109|TR2M_AGRRH Tryptophan 2-monooxygenase OS=Agrobacterium rhizogenes OX=359 GN=aux1 PE=3 SV=1",
                "MAGSSFTLPSTGSAPLDMMLIDDSDLLQLGLQQVFSKRYTETPQSRYKLTRRASPDVSSG")

    assert result == expected, f"Result: {result}\nExpected: {expected}"


@pytest.mark.parametrize("is_filter,db_key",
                         [(False, "with_fragment"),
                          (True, "no_fragment")])
def test_building_blast_db(temp_dir, seq_paths, expected_database, is_filter, db_key):
    output_filepath = temp_dir / "test_database.fasta"
    build_blast_db(seq_paths["seq_dir"],
                   output_filepath,
                   filter_fragment=is_filter)
    with open(output_filepath) as f1, open(expected_database[db_key]) as f2:
        result = f1.read()
        expected = f2.read()

    assert result == expected, f"Result: {result}\nExpected: {expected}"
