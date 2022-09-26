# Biofertilizer Prediction
## Aim
To identify potential bacteria species that may facilitate plant growth.
## Description
### Purpose of this package
Based on the assumption that the enzymes in related pathways (e.g., N-fixation, phosphate solubilization, plant hormone production) must exist, this package provides the pipeline to annotate the genome, filter out the desired enzyme products and map them to the custom-built pathway.
### Current Version
Able to process NCBI genome datasets (.fna format) and show the pathway completeness automatically. Now the custom-built pathway includes part of the bacteria IAA production pathway.
### Next Version
Complete the IAA pathway and maybe others.

## Basic Usage
*Note:*  
*To use this package, installation of **prodigal**, **blast** and some of the python modules is required (See the last section of README). Also, this package has only been tested locally. Dependency issues may occur if only this repository is copied to a brand new environment.*
### Set up blast database path
After the database has been made through `makeblastdb` command in `blast`, modify the `path` value in `config.toml` to tell the program which database is used for blastp alignment. (An absolute path is recommended)

### Run annotation and mapping from downloaded NCBI genome datasets
#### Command
```bash
python main.py ${PATH_TO_DIR_OR_FILE}
```
#### Output
- **tmp** folder with files from each intermediate step of this program.
- **result** folder with the result from enzyme mapping.   

### Run individual modules
#### Command
```bash
python module.py --[MODULE_NAME] ${ARGS_REQUIRED}
```
#### Output
See each module.

### Database building (For development only)
#### Command
```bash
python database_building.py --[MODULE_NAME] ${ARGS_REQUIRED}
```

## Software required
prodigal: <https://github.com/hyattpd/Prodigal>  
blast: <https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/>  
python module: `requirements.txt` will be added after a stable version is built.