from biopathpred.modules.match_enzyme import (match_enzyme_existence,
                                              reset_enzyme_and_pathway,
                                              traverse_enzyme_reaction)
from biopathpred.modules.pathway import enzyme_dict, pathway_dict


def test_match_enzyme_existence():
    filename = "tests/test_data/match_enzyme/GCF_match_enzyme_example.csv"
    match_enzyme_existence(filename, enzyme_dict)
    expected = [0, 11, 8, 6, 42]
    assert_list = [enzyme_dict[i].count == expected[i - 1] for i in range(1, 6)]
    assert all(assert_list)


def test_traverse_enzyme_reaction():
    reset_enzyme_and_pathway(enzyme_dict, pathway_dict)
    enzyme_num = [0, 1, 2, 3, 4, 0, 0, 0, 0, 1, 5, 6]
    for i in range(1, 13):
        if enzyme_num[i - 1] != 0:
            enzyme_dict[i].set_count(enzyme_num[i - 1])
    traverse_enzyme_reaction(pathway_dict[1], enzyme_dict, pathway_dict)
    expected = [True, False, True, True, True, False, False, False]
    assert_list = [pathway_dict[i].visited == expected[i - 1]
                   for i in range(1, 9)]
    assert all(assert_list)
