#!/bin/bash
mkdir -p ./.tmp/prokka
if [ -d "$1" ]; then
    filename=$(find "$1" -name "*.fna")
    for file in $filename
    do
        echo "Find $file"
        base_name=$(basename -s .fna "$file")
        prodigal -i "$file" -o "./.tmp/prokka/$base_name.genes" -a "./.tmp/prokka/$base_name.faa" 
    done
elif [ -f "$1" ]; then
    base_name=$(basename -s .fna "$1")
    prodigal -i "$file" -o "./.tmp/prokka/$base_name.genes" -a "./.tmp/prokka/$base_name.faa" 
else
    echo "Invalid input"
fi