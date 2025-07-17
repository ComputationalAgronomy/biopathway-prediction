#!/usr/bin/bash

# Check for required commands
for cmd in curl tar; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: Required command '$cmd' not found. Please install it."
        exit 1
    fi
done

if [ -f "pyproject.toml" ]; then
    :
elif [ -f "../pyproject.toml" ]; then
    cd ..
else
    echo "Error: Please run this script from the project root or a subdirectory directly beneath it."
    exit 1
fi

mkdir -p data data_positive data_negative

declare -A targets=(
    ["core_Acidobacteria"]="data"
    ["core_Actinobacteria"]="data"
    ["core_Bacteroidetes"]="data"
    ["core_Firmicutes"]="data"
    ["core_Proteobacteria"]="data"
    ["negative_validation"]="data_negative"
    ["positive_validation"]="data_positive"
)

for name in "${!targets[@]}"; do
    echo "== Downloading $name..."
    url="https://zenodo.org/records/15860571/files/${name}.tar.gz?download=1"
    downloaded_file="${name}.tar.gz"
    target_dir="${targets[$name]}"

    curl -fL -o "$downloaded_file" "$url"
    if [ $? -ne 0 ]; then
        echo "== Error: Failed to download $name."
        continue
    fi

    echo "== Extracting $name..."
    tar -xzf "$downloaded_file" -C "$target_dir"
    if [ $? -ne 0 ]; then
        echo "== Error: Failed to extract $name."
    fi

    echo "== Cleaning up $name..."
    rm "$downloaded_file"
done