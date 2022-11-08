#!/bin/bash
cpus=$4
filetype=".faa"
tmpfolder="$2"
db="$3"
mkdir -p $tmpfolder
echo "Start blastp alignment"
if [ -d "$1" ]; then
    filename=$(find "$1" -name "*$filetype")
    filecount=$(echo "$filename" | wc -w)
    count=0
    for file in $filename
    do
        count=$((count+1))
        echo -ne "Progress: $count/$filecount\r"
        base_name=$(basename -s "$filetype" "$file")
        diamond blastp -d ${db%.fasta} -q $file --outfmt 5 --xml-blord-format -o $tmpfolder/$base_name.xml 2> /dev/null
        # cat "$file" | parallel --gnu --plain -j $cpus --block-size 10K --recstart '>' --pipe blastp -query - -db "$db" -num_threads 1 -evalue 1e-10 -num_alignments 3 -outfmt 5 >> "$tmpfolder/$base_name.xml" 2> /dev/null
    done
elif [ -f "$1" ]; then
    base_name=$(basename -s "$filetype" "$1")
    diamond blastp -d ${db%.fasta} -q $1 --outfmt 5 --xml-blord-format -o $tmpfolder/$base_name.xml 2> /dev/null
    # cat "$1" | parallel --gnu --plain -j $cpus --block-size 10K --recstart '>' --pipe blastp -query - -db "$db" -num_threads 1 -evalue 1e-10 -num_alignments 3 -outfmt 5 >> "$tmpfolder/$base_name.xml" 2> /dev/null
else
    echo "Invalid input"
fi
echo "Finish blastp alignment"