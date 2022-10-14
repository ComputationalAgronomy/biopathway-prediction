# Biofertilizer Prediction

## Aim
To identify potential bacteria strains that may facilitate plant growth.

## Description
The potential and application of microbial products on crops have long been investigated in order to reduce the usage of synthetic fertilizers. Several mechanisms in promoting plant growth have been proposed and confirmed through field trials, including N-fixation, phosphage solubilization, phytohormone production and so on. Therefore, in this project we focus on the enzymes involved in these biological pathways. Based on the assumption that the enzymes in a certain biological pathway must exist for a microorganism to successfully catalyze the compounds available from the environment to accessible products for plants, this package provides the pipeline from microbial genome annotation to biological pathway mapping. This allows us to conduct a high-throughput screening from available genome datasets and constructs a model to evaluate the potential of individual microbial genomes. 

The current version is able to process genome datasets in NCBI format (i.e. `*.fna` format) and estimate the pathway completeness automatically. The current custom-built pathway includes part of the bacteria IAA production pathway.


## Basic Usage
### Annotation and mapping from downloaded NCBI genome datasets

```bash
python main.py INPUT_PATH
```
#### Options
`INPUT_PATH`: **a single .fna file** or **a folder that contains multiple .fna files**. 
#### Output
- **tmp** folder with files from each intermediate step of this program.
- **result** folder with the result from enzyme mapping.   


### Run individual modules
```bash
python module.py --MODULE_NAME ARGS_REQUIRED
```
#### Options
MODULE_NAME  
`--run_prodigal`, `--run_blast`, `--parse_ncbi_xml`, `--best_blast`, `--match_enzyme`
Each module handles the output from the previous one. Use `python module.py -h` to see the arguments required. The `INPUT_PATH` can be a file or directory.

#### Output
- **module_output** folder with a MODULE_NAME subfolder that contains the result. 

### Database building (For development only)
*Note: this section entails modification of `pathway.py`, otherwise the enzyme mapping will be incorrect.* 
#### Command
```bash
python database_building.py --MODULE_NAME ARGS_REQUIRED
```
#### Options
MODULE_NAME  
`--add_id`, `--get_entry`, `--filter_database`  
Use `python database_building.py -h` to see the arguments required.  
- Building a custom UniProt database:  
A tag with the format `{enzyme_id}_{enzyme_code}` (e.g. 1_IAM, 2_IPA) is added to the given UniProt database entries.  
- Still using a larger UniProt database:  
UniProt IDs are then extracted from the custom database entries and used as filters, followed by adding the labelled entries back.  




## Example usage and output
- Example input
```bash
# a single file
python main.py example_genome.fna
# multiple files in a folder
python main.py example_dataset/
```
- Example output
```bash
Compound list:
trp: True # existence of the compound in the pathway
iam_1: True
indole-3-acetic-acid: False
...

Enzyme list:
trp_iam_1: 0 # no. of matching from the best blastp result
iam_1_indole: 1
trp_ipa_1: 1
...
```


## Installation
*Note:*  
*To use this package, installation of **prodigal**, **blast** and some of the python modules is required (See the software requirement section). Also, this package has only been tested locally. Dependency issues may occur if only this repository is copied to a brand new environment.*

### Testing
```
pytest
# With coverage
pytest --cov=src
```


### Set up blast database path
After the database has been made through `makeblastdb` command in `blast`, modify the `path` value in `config.toml` to tell the program which database is used for blastp alignment. (An absolute path is recommended)



### Software requirement
prodigal: <https://github.com/hyattpd/Prodigal>  
blast: <https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/>  
python module: `requirements.txt` will be added after a stable version is built.

## Roadmap
### Next Version
Complete the IAA pathway and maybe others.
