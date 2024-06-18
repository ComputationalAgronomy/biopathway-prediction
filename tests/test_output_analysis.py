import tempfile
from pathlib import Path

from biopathpred.modules.result_summary import result_summary

DATA_DIR = Path(__file__).parent / "test_data/mapping_analysis/test_data"
EXPECTED_DIR = Path(__file__).parent / "test_data/mapping_analysis/expected"


def test_enzyme_mapping_analysis():
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdirname = Path(tmpdirname)
        result_summary(DATA_DIR, tmpdirname)
        with open(EXPECTED_DIR / "compound_output.csv") as expected, \
                open(tmpdirname / "compound_output.csv") as output:
            assert expected.read() == output.read()
        with open(EXPECTED_DIR / "enzyme_output.csv") as expected, \
                open(tmpdirname / "enzyme_output.csv") as output:
            assert expected.read() == output.read()
        with open(EXPECTED_DIR / "prediction_output.csv") as expected, \
                open(tmpdirname / "prediction_output.csv") as output:
            assert expected.read() == output.read()
