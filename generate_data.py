#!/usr/bin/env python

import argparse
import generate_assembly_functions
import generate_source_functions
import re
import os

parser = argparse.ArgumentParser(description = "Generate data for translating \
        assembly to source code using the Linux Kernel")
parser.add_argument("--object_file", type=str, required=True)
parser.add_argument("--source_directory", type=str)
parser.add_argument("--output_directory", type=str, default="output")


def main():
    args = parser.parse_args()

    output_directory = args.output_directory

    assembly_functions = generate_assembly_functions.generate(args.object_file)
    source_functions = generate_source_functions.generate(args.source_directory)

    def strip_for_file_name(original):
        return re.sub("[^0-9A-Za-z]+", "", original)

    print("Writing out assembly functions")
    for function in assembly_functions:
        file_name = strip_for_file_name(function.name) + "_assembly"
        with open(os.path.join(output_directory, file_name), 'w') as f:
            for line in function.lines:
                f.write(line + "\n")

    print("Writing out source functions")
    for function in source_functions:
        file_name = strip_for_file_name(function.name) + "_source"

        with open(os.path.join(output_directory, file_name), 'w') as f:
            for line in function.body:
                f.write(line)


if __name__ == "__main__":
    main()
