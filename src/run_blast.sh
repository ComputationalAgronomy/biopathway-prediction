#!/bin/bash
cpus=2
filetype=".faa"
db="./blast_test/uniprot_sprot.fasta"
outfolder="./.tmp/blastp"
mkdir -p ./.tmp/blastp
if [ -d "$1" ]; then
    filename=$(find "$1" -name "*$filetype")
    for file in $filename
    do
        echo "Find $file"
        base_name=$(basename -s "$filetype" "$file")
        blastp -query "$file" -db "$db" -evalue 1e-10 -num_alignments 3 -outfmt 5 -out "$outfolder/$base_name.xml" 
    done
elif [ -f "$1" ]; then
    base_name=$(basename -s "$filetype" "$1")
    cat "$1" | parallel -j $cpus --recstart '>' --pipe blastp -query "$1" -db "$db" -num_threads 1 -evalue 1e-10 -num_alignments 3 -outfmt 5 -out "$outfolder/$base_name.xml"
else
    echo "Invalid input"
fi