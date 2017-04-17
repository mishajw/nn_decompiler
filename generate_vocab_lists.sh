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

echo "Creating cpp vocab"
get_words output/cpp > output/cpp_vocab.txt

echo "Done"

