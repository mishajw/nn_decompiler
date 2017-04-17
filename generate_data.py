#!/usr/bin/env python

import argparse
import generate_assembly_functions
import generate_source_functions
import re
import os
from itertools import islice

parser = argparse.ArgumentParser(
    description="Generate data for translating assembly to source code using the Linux Kernel")
parser.add_argument("--object_file", type=str, required=True)
parser.add_argument("--source_directory", type=str)
parser.add_argument("--output_directory", type=str, default="output")
parser.add_argument("--max_functions", type=int, default=None)


def main():
    args = parser.parse_args()

    output_directory = args.output_directory
    max_functions = args.max_functions

    assembly_functions = generate_assembly_functions.generate(args.object_file)
    source_functions = generate_source_functions.generate(args.source_directory)

    for path in [os.path.join(output_directory, subdirectory) for subdirectory in ["asm", "c"]]:
        if not os.path.exists(path):
            print("Creating directory %s because it doesn't exist" % path)
            os.makedirs(path)

    def strip_for_file_name(original):
        return re.sub("[^0-9A-Za-z_]+", "", original)

    print("Writing out assembly functions")
    for function in islice(assembly_functions, max_functions):
        file_name = strip_for_file_name(function.name) + ".asm"
        with open(os.path.join(output_directory, "asm", file_name), 'w') as f:
            f.write("<%s>:\n" % function.name)
            for line in function.lines:
                f.write(line + "\n")

    print("Writing out source functions")
    for function in islice(source_functions, max_functions):
        file_name = strip_for_file_name(function.name) + ".c"

        with open(os.path.join(output_directory, "c", file_name), 'w') as f:
            for line in function.body:
                f.write(line)


if __name__ == "__main__":
    main()
