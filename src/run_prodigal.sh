#!/bin/bash
tmpfolder=${2-./tmp/prodigal}
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
elif [ -f "$1" ]; then
    base_name=$(basename -s .fna "$1")
    prodigal -i "$1" -o "$tmpfolder/$base_name.genes" -a "$tmpfolder/$base_name.faa" 2> /dev/null 
else
    echo "Invalid input"
fi
echo "Finish prodigal gene prediction"
