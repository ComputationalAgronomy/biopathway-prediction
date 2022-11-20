import os
import pandas as pd
import pytest

from src.match_enzyme import (match_enzyme_existence, traverse_enzyme_reaction,
                              reset_enzyme_and_pathway, existence_score_model)
from src.pathway import enzyme_list, pathway_list

def test_match_enzyme_existence():
    filename = "tests/test_data/GCF_match_enzyme_example.csv"
    match_enzyme_existence(filename, enzyme_list)
    expected = [0, 11, 8, 6, 42]
    assert_list = [enzyme_list[i].count == expected[i-1] for i in range(1, 6)]
    assert all(assert_list)

def test_traverse_enzyme_reaction():
    reset_enzyme_and_pathway(enzyme_list, pathway_list)
    enzyme_num = [0, 1, 2, 3, 4, 0, 0, 0, 0, 1, 5, 6]
    for i in range(1, 13):
        if enzyme_num[i-1] != 0:
            enzyme_list[i].set_count(enzyme_num[i-1])
    traverse_enzyme_reaction(pathway_list[1], enzyme_list, pathway_list)
    expected = [True, False, True, True, True, False, False, False]
    assert_list = [pathway_list[i].visited == expected[i-1] for i in range(1, 9)]
    assert all(assert_list)

