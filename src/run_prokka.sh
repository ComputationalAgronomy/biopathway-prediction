#!/bin/bash
if [ -d "$1" ]; then
    filename=$(find "$1" -name "*.fna")
    for file in $filename
    do
        echo "Find $file"
        base_name=$(basename -s .fna "$file")
        prokka --norrna --notrna --cpus 0 --prefix "$base_name" "$file"
    done
elif [ -f "$1" ]; then
    base_name=$(basename -s .fna "$1")
    prokka --norrna --notrna --cpus 0 --prefix "$base_name" "$1"
else
    echo "Invalid input"
fi
