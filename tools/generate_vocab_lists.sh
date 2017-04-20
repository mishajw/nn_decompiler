#!/usr/bin/env bash

get_words() {
  source_directory=$1

  # `cat` every file
  find $source_directory -type f | xargs cat | \
    # Print all words
    grep -Po '\w+|[^\w\s]+' | \
    # Get frequencies
    sort | uniq -c | sort -hr
}

echo "Creating asm vocab"
get_words output/asm > output/asm_vocab.txt

echo "Creating c vocab"
get_words output/c > output/c_vocab.txt

echo "Done"

