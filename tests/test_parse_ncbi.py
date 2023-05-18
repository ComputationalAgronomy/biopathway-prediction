import os
import tempfile

import pytest

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

    title = "gnl|BL_ORD_ID|19 sp|Q9C969|ISS1_ARATH 3~~~IPA1~~~Aromatic aminotransferase ISS1 OS=Arabidopsis thaliana OX=3702 PE=1 SV=1"
    alignment_info = parse_alignment_title(title)
    expected = "Q9C969,3,IPA1,Aromatic aminotransferase ISS1,Arabidopsis thaliana,1,-"
    assert alignment_info == expected


def test_parse_ncbi():
    testfilepath = "tests/test_data/GCF_example.xml"
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfilename = "tmp_parse_ncbi.csv"
        tmpfilepath = os.path.join(tmpdirname, tmpfilename)
        parse_blast(testfilepath, tmpfilepath)
        with open(tmpfilepath, "r") as f:
            results = f.read()
    expected = (
        "id,start,end,alignment_id,enzyme_id,enzyme_code,product,organism,existence,gene,score,evalue,identity,coverage\n"
        "NZ_CP012401.1_70,81257,82396,Q0KDL6,5,IPA3,Alcohol dehydrogenase,Cupriavidus necator (strain ATCC 17699 / DSM 428 / KCTC 22496 / NCIMB 10442 / H16 / Stanier 337),1,adh,118.627,5.7216e-32,30.491,88.158\n"
        "NZ_CP012401.1_70,81257,82396,P14940,5,IPA3,Alcohol dehydrogenase,Cupriavidus necator,3,adh,117.857,1.05788e-31,30.491,88.158\n"
    )
    # os.remove(tmpfile)
    assert results == expected

    testfilepath = "tests/test_data/no_this_file.xml"
    tmpfile = "tmp_parse_ncbi.csv"
    with pytest.raises(SystemExit) as excinfo:
        parse_blast(testfilepath, tmpfile)
    assert True
