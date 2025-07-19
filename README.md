# BCPIP - Biological Compound Predictor via Integrated Pathways

## Aim

To identify potential bacterial strains that may produce indole-3-acetic acid (IAA) and thus facilitate plant growth through an efficient computational screening approach.

## Description
BCPIP (Biological Compound Predictor via Integrated Pathways) is a bioinformatics pipeline that predicts a bacterium's potential to produce specific biological compounds based on its genome sequence. The pipeline predicts biological compound synthesis potential by analyzing multiple metabolic pathways.

The overview of the workflow is as follows:
1. **Gene Prediction**: Takes bacterial genomes as input and predicts protein-coding genes.
2. **Enzyme Mapping**: Compares the predicted genes against a curated database of enzymes from specific, predefined biological pathways using DIAMOND.
3. **Compound Prediction**: Based on the enzyme matches, predicts the likelihood that the bacterium can synthesize the final compound using multiple pathways.

The current version is optimized for the Indole-3-Acetic Acid (IAA) biosynthesis pathway, allowing for high-throughput screening of bacterial genomes to identify potential plant-growth-promoting strains. The output provides a clear summary of predicted compound presence for each genome.


### Background
Microbial products have been extensively studied for plant growth promotion to reduce synthetic fertilizer usage. Several plant growth-promoting mechanisms have been confirmed, and this project focuses on enzymes involved in these biological pathways, using auxin biosynthesis as an example. Based on the assumption that specific pathway enzymes must be present for microorganisms to successfully synthesize the compounds. This software provides a pipeline to estimate the likelihood of synthesizing compounds from genomic data. This enables high-throughput screening of genome datasets to evaluate the metabolic potential of individual bacterial strains.


## Installation

1. **Create and activate a conda environment:**
   ```bash
   conda create -n bcpip python
   conda activate bcpip
   ```

2. **Install the package:**
   ```bash
   pip install .
   ```

**Note:** This tool requires **Prodigal** and **DIAMOND** to be installed. Please see the `Software Requirements` section below for instructions.

### Software Requirements

Before running the prediction pipeline, you must install the following software and specify their paths in the `config.toml` file:

- **Prodigal:** [https://github.com/hyattpd/Prodigal](https://github.com/hyattpd/Prodigal)
- **DIAMOND:** [https://github.com/bbuchfink/diamond](https://github.com/bbuchfink/diamond)

After downloading, place the executables in the `bin/` directory or any other location and update the `prodigal_path` and `diamond_path` in your `config.toml` accordingly.

## Basic Usage

**Note:** Always run commands from the project's root directory (the one containing `config.toml`), or from a location where it can be discovered in a parent directory.

### Run prediction pipeline on downloaded NCBI genome datasets

```
bcpip -i INPUT_DIR -o OUTPUT_DIR
```

#### Options

`INPUT_DIR`: **a single .fna file** or **a folder that contains multiple .fna files**.
`OUTPUT_DIR`: where the results are stored.

#### Output

- **match_enzyme_result** folder stores prediction result for each genome.
- **result_summary** folder stores the summary for all genomes.

### Run individual modules

```
bcpip MODULE_NAME ARGS_REQUIRED
```

#### Options

MODULE_NAME
`prodigal`, `blastp`, `parse_xml`, `best_blast`, `match_enzyme`, `result_summary`

Each module handles the output from the previous pipeline stage. Use `-h` to see the arguments required.

### Workflow reproduction

See `notebooks/MS_workflow.ipynb` for instructions on reproducing the results in the paper from raw genome sequences. A script version of the workflow is available in `MS_workflow`.

### Database building (For development only)

_Note: this section entails modification of `pathway.py`, otherwise the enzyme mapping will be incorrect._

See `notebooks/build_blast_database.ipynb`

### Available commands

```
usage: bcpip [-h] [-o OUTPUT] [--cpus CPUS] [-i INPUT] [-d DATABASE] [-c CRITERIA] [-f [FILTER ...]] [-m MODEL] [--verbose] [--debug]
                   {prodigal,blastp,parse_xml,best_blast,match_enzyme,result_summary,build_db} ...

positional arguments:
  {prodigal,blastp,parse_xml,best_blast,match_enzyme,result_summary,build_db}
                        module name

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output path
  --cpus CPUS           number of processes to be created (default: available_threads / 2)
  -i INPUT, --input INPUT
                        input a file or directory path
  -d DATABASE, --database DATABASE
                        database path
  -c CRITERIA, --criteria CRITERIA
                        selection criteria
  -f [FILTER ...], --filter [FILTER ...]
                        filter options
  -m MODEL, --model MODEL
                        model name
  --verbose             print match_enzyme result to screen
  --debug               keep all intermediate files if specified
```

## Example usage and output

- Example input

```
# a single file
bcpip -i example_data/GCF_000014005.1_ASM1400v1_genomic.fna -o example_output/
# multiple files in a folder
bcpip -i example_data/ -o example_output/
```

- Example output (`GCF_000014005.1_ASM1400v1_genomic.txt`)

```
Compound list:
trp: 1.0
iam_1: 0.0
iaa: 0.292642
ipa_1: 0.238995
ipa_2: 0.251905
tam_1: 0.826323
iaox: 0.0
ian_1: 0.0

Enzyme list:
trp_iam_1: 0
iam_1_iaa: 0.964073
trp_ipa_1: 0.238995
ipa_1_2: 0
ipa_2_iaa: 0.999867
ipa_1_iaa: 0.228024
trp_tam_1: 0.826323
tam_1_ipa_2: 0.30485
trp_iaox: 0
iaox_ian_1: 0
ian_1_iaa: 0.411662
ian_1_iam_1: 0
```
