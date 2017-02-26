#!/usr/bin/env python

import argparse
import generate_assembly_files
import generate_source_files

parser = argparse.ArgumentParser(description = "Generate data for translating \
        assembly to source code using the Linux Kernel")
parser.add_argument("--object_file", type=str, required=True)
parser.add_argument("--source_directory", type=str)
parser.add_argument("--output_directory", type=str, default="output")


def main():
    args = parser.parse_args()

    assembly_functions = generate_assembly_files.generate(args.object_file)
    source_functions = generate_source_files.generate(args.source_directory)

    for function in assembly_functions:
        print(function.name)

    for function in source_functions:
        print(function.name)



if __name__ == "__main__":
    main()

