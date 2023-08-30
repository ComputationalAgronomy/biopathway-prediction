import os

import pytest

from biopathpred.database_building.database_utils import split_fasta


def test_split_fasta():
    file = "tests/test_data/fasta_sequence_example.fasta"
    results = split_fasta(file)
    expected = [[">sp|O49342|C71AD_ARATH 10~~~IAN1-1~~~Indoleacetaldoxime dehydratase OS=Arabidopsis thaliana OX=3702 GN=CYP71A13 PE=1 SV=1\n",
                 "MEMILSISLCLTTLITLLLLRRFLKRTATKVNLPPSPWRLPVIGNLHQLSLHPHRSLRSL\n"],
                [">sp|P0A3V3|TR2M_RHIRD Tryptophan 2-monooxygenase OS=Rhizobium radiobacter OX=358 GN=tms1 PE=3 SV=1\n",
                 "MSASPLLDNQCDHLPTKMVDLTMVDKADELDRRVSDAFLEREASRGRRITQISTECSAGL\n"],
                [">sp|Q09109|TR2M_AGRRH Tryptophan 2-monooxygenase OS=Agrobacterium rhizogenes OX=359 GN=aux1 PE=3 SV=1\n",
                 "MAGSSFTLPSTGSAPLDMMLIDDSDLLQLGLQQVFSKRYTETPQSRYKLTRRASPDVSSG\nMSASPLLDNQCDHLPTKMVDLTMVDKADELDRRVSDAFLEREASRGRRITQISTECSAGL\n"]]
    assert results == expected

