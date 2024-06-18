# Biopathway Prediction

## Aim
To identify potential bacteria strains that may produce IAA and thus facilitate plant growth.

## Description
The potential and application of microbial products on crops have long been investigated in order to reduce the usage of synthetic fertilizers. Several mechanisms in promoting plant growth have been proposed and confirmed through field trials, including N-fixation, phosphate solubilization, phytohormone production and so on. Therefore, in this project we focus on the enzymes involved in these biological pathways, using auxin biosynthesis pathway as an example. Based on the assumption that the enzymes in a certain biological pathway must exist for a microorganism to successfully catalyze the compounds available from the environment to accessible products for plants, this package provides the pipeline from microbial genome annotation to biological pathway mapping. This allows us to conduct a high-throughput screening from available genome datasets and constructs a model to evaluate the potential of individual microbial genomes. 

The current version is able to process genome datasets downloaded from NCBI (i.e. .fna format) and estimate the pathway completeness automatically. The current custom-built pathway includes part of the bacteria IAA production pathway.

## Installation
```
conda create -n biopathpred python
conda activate biopathpred
pip install -e .
```
*Note:*  
*To use this package, installation of **prodigal**, **diamond** are required.*

### Software requirement
Put the following two programs into `bin` and specify their paths in `config.toml`

prodigal: <https://github.com/hyattpd/Prodigal> \
diamond: <https://github.com/bbuchfink/diamond>  


## Basic Usage
### Run prediction pipeline on downloaded NCBI genome datasets
```
biopathpred -i INPUT_DIR -o OUTPUT_DIR
```
#### Options
`INPUT_DIR`: **a single .fna file** or **a folder that contains multiple .fna files**.
`OUTPUT_DIR`: where the results are stored. 
#### Output
- **match_enzyme_result** folder stores prediction result for each genome. 
- **result_summary** folder stores the summary for all genomes.   


### Run individual modules
```
biopathpred MODULE_NAME ARGS_REQUIRED
```
#### Options
MODULE_NAME  
`prodigal`, `blastp`, `parse_xml`, `best_blast`, `match_enzyme`, `result_summary`

Each module handles the output from the previous pipeline stage. Use `-h` to see the arguments required.


### Database building (For development only)
*Note: this section entails modification of `pathway.py`, otherwise the enzyme mapping will be incorrect.* 

See `notebooks/build_blast_database.ipynb`


### Available commands

```
usage: biopathpred [-h] [-o OUTPUT] [--cpus CPUS] [-i INPUT] [-d DATABASE] [-c CRITERIA] [-f [FILTER ...]] [-m MODEL] [--verbose] [--debug]
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
biopathpred -i example_data/GCF_000014005.1_ASM1400v1_genomic.fna -o example_output/
# multiple files in a folder
biopathpred -i example_data/ -o example_output/
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
