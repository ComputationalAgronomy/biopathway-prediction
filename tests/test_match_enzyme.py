import os
import pandas as pd
import pytest

from src.match_enzyme import match_enzyme_existence, traverse_enzyme_reaction
from src.pathway import ENZYME_LIST, PATHWAY_LIST

def test_match_enzyme_existence():
    filename = "tests/test_data/GCF_match_enzyme_example.csv"
    match_enzyme_existence(filename, ENZYME_LIST)
    expected = [0, 11, 8, 6, 42]
    assert_list = [ENZYME_LIST[i].count == expected[i-1] for i in range(1, 6)]
    assert all(assert_list)

def test_traverse_enzyme_reaction():
    enzyme_num = [0, 1, 2, 3, 4, 0, 0, 0, 0, 0, 5, 6]
    for i in range(1, 13):
        ENZYME_LIST[i].set_count(enzyme_num[i-1])
    traverse_enzyme_reaction(1, ENZYME_LIST, PATHWAY_LIST)
    expected = [True, False, True, True, True, False, False, False]
    assert_list = [PATHWAY_LIST[i].visited == expected[i-1] for i in range(1, 9)]

