# Biofertilizer Prediction
## Basic Usage
### Parse gff or gff3 annotation files
#### Command
```bash
python parse_gff.py ${PATH_TO_DIR_OR_FILE}
```
#### Output
- .csv files under the folder "output"
- Column: 
    - NCBI accession number
    - Feature Start (Protein, RNA, ...)
    - Feature End
    - EC number (if any)
    - Product
  
### Compare annotation files (merge them)
Command
```bash
python diff_annotation.py ${PATH_TO_FILE_1} ${PATH_TO_DIR_OR_FILE_2}
``` 
#### Output
- Outer join two .csv files based on "accession number", "feature start" and "feature end".