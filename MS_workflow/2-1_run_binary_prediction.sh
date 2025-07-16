#!/usr/bin/bash
# Note: Ensure that the binaries of **prodigal** and **diamond** are
# downloaded and their full paths are set in `config.toml`
# before running this script.
#
# Results
# A summary of the prediction results is saved to `output_binary/result_summary`.  
# The file `prediction_output.csv` contains the prediction scores for IAA production for each genome.
# Summary statistics for all genomes are provided in `compound_output.csv` and `enzyme_output.csv`.  
# Individual predictions for each genome are saved in `output_binary/match_enzyme_result`.

if [ -f "pyproject.toml" ]; then
    :
elif [ -f "../pyproject.toml"]; then
    cd ..
else
    echo "Error: Please run this script from the project root or a subdirectory directly beneath it."
fi

python -m pip install .
python biopathpred/utils/rename_sequence_label.py data fna
biopathpred -i data/ -o output_binary/ -m binary -f coverage=50 -c score