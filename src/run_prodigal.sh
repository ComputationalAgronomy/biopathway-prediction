#!/bin/bash
tmpfolder="./tmp/prokka"
mkdir -p $tmpfolder
if [ -d "$1" ]; then
    filename=$(find "$1" -name "*.fna")
    filecount=$(echo "$filename" | wc -w)
    for file in $filename
    do
        count=$((count+1))
        echo -ne "Progress: $count/$filecount\r"
        base_name=$(basename -s .fna "$file")
        prodigal -i "$file" -o "$tmpfolder/$base_name.genes" -a "$tmpfolder/$base_name.faa" 2> /dev/null
    done
    echo "Finish prodigal gene prediction"
elif [ -f "$1" ]; then
    base_name=$(basename -s .fna "$1")
    prodigal -i "$file" -o "$tmpfolder/$base_name.genes" -a "$tmpfolder/$base_name.faa" 2> /dev/null 
    echo "Finish prodigal gene prediction"
else
    echo "Invalid input"
fi