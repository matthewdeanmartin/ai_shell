#!/bin/bash
set -euo pipefail
bash --version

# Set tool locations
TIDY="node_modules/.bin/tidy-markdown"

echo "Working with these files"
FILES=$(find . -type f -name "*.md" ! -path "./node_modules/*")
for file in $FILES; do
    echo "$file"
done
echo

echo
echo "Formatting markdown files with mdformat"
echo
for file in $FILES; do
    poetry run mdformat "$file"
done


echo
echo "Are the links okay?"
echo
poetry run linkcheckMarkdown content
