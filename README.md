# Biofertilizer Prediction

## Aim
To identify potential bacteria strains that may facilitate plant growth.

## Description
[An intro on why do we want to work with biological pathways]. Based on the assumption that enzymes in biological pathways (e.g., N-fixation, phosphate solubilization, plant hormone production) must exist, this package provides
The pipeline consists of the following key steps; annotate the genome, filter out the desired enzyme products, and map them to a specific biological pathway.

The current version is able to process genome datasets in NCBI format (i.e. `*.fna` format) and estimate the pathway completeness automatically. The custom-built pathway includes part of the bacteria IAA production pathway.


## Basic Usage
### Annotation and mapping from downloaded NCBI genome datasets

```bash
python main.py PATH_TO_DIR_OR_FILE
```
#### Options
`PATH_TO_DIR_OR_FILE`: Steven assumes it's genome file(s) in FASTA format?
#### Output
- **tmp** folder with files from each intermediate step of this program.
- **result** folder with the result from enzyme mapping.   


### Run individual modules
```bash
python module.py --MODULE_NAME ARGS_REQUIRED
```
#### Options
TODO: List the MODULE_NAME that are currently available
#### Output
See each module.
TODO: Remove this section for now unless there are some info.


### Database building (For development only)
#### Command
```bash
python database_building.py --MODULE_NAME ARGS_REQUIRED
```
#### Options
TOOD: ARGS_REQUIRED


## Example usage and output
- Example input
- `python main.py example_genome.fna`
- Example output
- Summary of the output


## Installation
*Note:*  
*To use this package, installation of **prodigal**, **blast** and some of the python modules is required (See the software requirement section). Also, this package has only been tested locally. Dependency issues may occur if only this repository is copied to a brand new environment.*

### Set up blast database path
After the database has been made through `makeblastdb` command in `blast`, modify the `path` value in `config.toml` to tell the program which database is used for blastp alignment. (An absolute path is recommended)

### Software requirement
prodigal: <https://github.com/hyattpd/Prodigal>  
blast: <https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/>  
python module: `requirements.txt` will be added after a stable version is built.




## Roadmap
### Next Version
Complete the IAA pathway and maybe others.
