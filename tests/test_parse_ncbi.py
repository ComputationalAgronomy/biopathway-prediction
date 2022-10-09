import pytest
from src import parse_ncbi_xml
from src.parse_ncbi_xml import (parse_alignment_title, parse_blast,
                                parse_product_regex, parse_product_split)


def test_parse_product_split():

    data = "PartA~~~P ar t  B~~~p~a=r(t)3"
    results = parse_product_split(data)
    expected = ("PartA", "P ar t  B", "p~a=r(t)3")
    assert results == expected

    data = "single"
    results = parse_product_split(data)
    expected = (None, None, "single")
    assert results == expected


def test_parse_product_regex():

    data = "PartA~~~P ar t  B~~~p~a=r(t)3"
    results = parse_product_regex(data)
    expected = ("PartA", "P ar t  B", "p~a=r(t)3")
    assert results == expected

    data = "single"
    results = parse_product_regex(data)
    expected = (None, None, "single")
    assert results == expected


def test_parse_product_regex_exception():

    data = "single~~~double"
    with pytest.raises(ValueError) as excinfo:
        parse_product_regex(data)
    assert "Invalid database product format" == str(excinfo.value)


def test_parse_alignment_title():
    title = "gnl|BL_ORD_ID|19 sp|Q9C969|ISS1_ARATH 3~~~IPA1~~~Aromatic aminotransferase ISS1 OS=Arabidopsis thaliana OX=3702 GN=ISS1 PE=1 SV=1"
    alignment_info = parse_alignment_title(title)
    expected = "Q9C969,3,IPA1,Aromatic aminotransferase ISS1,Arabidopsis thaliana,1,ISS1"
    assert alignment_info == expected

def test_parse_ncbi():
    # TODO
    filename = "tests/test_data/GCF_example.xml"
    # parse_blast(filename)