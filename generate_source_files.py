#!/usr/bin/env python

import os


def generate(source_directory):
    for file in get_source_files(source_directory):
        functions = get_functions_from_source(file)


def get_functions_from_source(file_name):
    return []


def get_source_files(source_directory):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith(".h") or file.endswith(".c"):
                yield os.path.join(root, file)

