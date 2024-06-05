#!/bin/bash

# Directory containing the PDF files
DIR=$1

# Check if the directory is provided
if [ -z "$DIR" ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Check if the directory exists
if [ ! -d "$DIR" ]; then
  echo "Directory $DIR does not exist."
  exit 1
fi

# Iterate over the 4 PDF files
for i in {1..4}; do
  for j in {1..250}; do
    cp "$DIR/$i.pdf" "$DIR/${i}_${j}.pdf"
    echo "Created copy $j of $i.pdf"
  done
done

echo "250 copies of each PDF created successfully."
