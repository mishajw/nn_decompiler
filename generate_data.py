#!/usr/bin/env python

import argparse
import generate_assembly_files
import generate_source_files

parser = argparse.ArgumentParser(description = "Generate data for translating \
        assembly to source code using the Linux Kernel")
parser.add_argument("--object_file", type=str)
parser.add_argument("--output_directory", type=str, default="output")


def main():
    args = parser.parse_args()

    generate_assembly_files.generate()
    generate_source_files.generate()


if __name__ == "__main__":
    main()

