#!/usr/bin/env python

import argparse
import os
import re
import sys

word_regex = re.compile("\w+|[^\w\s]+")

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
parser.add_argument("--new_line_token", type=str, default="<newline>")

def main():
    args = parser.parse_args()

    all_words = []

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    asm_output_path = os.path.join(args.output, "asm_output.txt")
    c_output_path = os.path.join(args.output, "c_output.txt")

    # Open the output files
    with open(asm_output_path, 'w') as asm_output_file, open(c_output_path, 'w') as c_output_file:
        # Take in file names from stdin
        for file_name in sys.stdin:
            file_name = file_name.strip()

            # Get the paths of the asm and c files
            asm_path = os.path.join(args.input, "asm", file_name + ".asm")
            c_path = os.path.join(args.input, "c", file_name + ".c")

            # Check they exist
            if not os.path.isfile(asm_path) or not os.path.isfile(c_path):
                print("Couldn't find files for %s at %s and %s" % (file_name, asm_path, c_path))
                continue

            # Get their output
            with open(asm_path, 'r') as input_file:
                asm_output = list(parse_file(input_file, args.new_line_token))
            with open(c_path, 'r') as input_file:
                c_output = list(parse_file(input_file, args.new_line_token))

            # Write them out in a single line
            asm_output_file.write(" ".join(asm_output) + "\n")
            c_output_file.write(" ".join(c_output) + "\n")


def parse_file(f, new_line_token):
    for line in f:
        for word in word_regex.findall(line):
            yield word

        yield new_line_token


if __name__ == "__main__":
    main()

