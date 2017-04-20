#!/usr/bin/env bash

if [[ $# != 2 ]]; then
  echo "Usage: $0 <object file> <output file>"
  exit
fi

object_file="$1"
output_file="$2"

objdump -d $object_file | grep -Eo '<([A-Za-z_]+)>:' | sed -E 's/(<|>|\:)//g' > $output_file

