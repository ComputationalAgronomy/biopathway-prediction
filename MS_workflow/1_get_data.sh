#!/usr/bin/bash
if [ -f "pyproject.toml" ]; then
    :
elif [ -f "../pyproject.toml"]; then
    cd ..
else
    echo "Error: Please run this script from the project root or a subdirectory directly beneath it."
fi

mkdir -p data
mkdir -p positive_data
mkdir -p negative_data

files=(
    core_Acidobacteria
    core_Actinobacteria
    core_Bacteroidetes
    core_Firmicutes
    core_Proteobacteria
    negative_validation
    positive_validation
)

declare -A targets=(
    ["core_Acidobacteria"]="data"
    ["core_Actinobacteria"]="data"
    ["core_Bacteroidetes"]="data"
    ["core_Firmicutes"]="data"
    ["core_Proteobacteria"]="data"
    ["negative_validation"]="negative_data"
    ["positive_validation"]="positive_data"
)

for name in "${!targets[@]}"; do
    echo "Downloading $name..."
    url="https://zenodo.org/records/15860571/files/${name}.tar.gz?download=1"
    downloaded_file="${name}.tar.gz"
    target_dir="${targets[$name]}"

    curl -fL -o "$downloaded_file" "$url"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download $name."
        continue
    fi

    echo "Extracting $name..."
    tar -xzf "$downloaded_file" -C "$target_dir"

    echo "Cleaning up $name..."
    rm "$downloaded_file"