import os
import pytest

import tempfile
import filecmp
from scripts.output_analysis.enzyme_mapping_analysis import enzyme_mapping_analysis

current_dir = os.path.dirname(__file__)

def test_enzyme_mapping_analysis():
    with tempfile.TemporaryDirectory() as tmpdirname:
        enzyme_mapping_analysis(
            "tests/test_data/enzyme_mapping_analysis/test_data",
            tmpdirname)
        cmp_compound = filecmp.cmp(
           "tests/test_data/enzyme_mapping_analysis/expected/compound_output.csv",
            os.path.join(tmpdirname, "compound_output.csv"))
        cmp_enzyme = filecmp.cmp(
            "tests/test_data/enzyme_mapping_analysis/expected/enzyme_output.csv",
            os.path.join(tmpdirname, "enzyme_output.csv"))
        cmp_prediction = filecmp.cmp(
            "tests/test_data/enzyme_mapping_analysis/expected/prediction_output.csv",
            os.path.join(tmpdirname, "prediction_output.csv"))
    
    assert all([cmp_compound, cmp_enzyme, cmp_prediction])


