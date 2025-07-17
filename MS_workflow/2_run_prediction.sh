#!/usr/bin/bash
# Note: Ensure that the binaries of **prodigal** and **diamond** are
# downloaded and their full paths are set in `config.toml`
# before running this script.
#
# Results
# A summary of the prediction results is saved to `output_logistic/result_summary`.
# The file `prediction_output.csv` contains the prediction scores for IAA production for each genome.
# Summary statistics for all genomes are provided in `compound_output.csv` and `enzyme_output.csv`.
# Individual predictions for each genome are saved in `output_logistic/match_enzyme_result`.


if [ -f "pyproject.toml" ]; then
    :
elif [ -f "../pyproject.toml" ]; then
    cd ..
else
    echo "Error: Please run this script from the project root or a subdirectory directly beneath it."
    exit 1
fi

MODEL_TYPE=$1

if [ "$MODEL_TYPE" != "binary" ] && [ "$MODEL_TYPE" != "logistic" ]; then
    echo "Error: Invalid model type. Please use 'binary' or 'logistic'."
    echo "Usage: $0 [binary|logistic]"
    exit 1
fi

INPUT_DIR="data"
OUTPUT_DIR="output_${MODEL_TYPE}"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

python -m pip install .
python biopathpred/utils/rename_sequence_label.py data fna
biopathpred -i ${INPUT_DIR} -o ${OUTPUT_DIR} -m ${MODEL_TYPE} -f coverage=50 -c score

