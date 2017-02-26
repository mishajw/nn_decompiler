#!/usr/bin/env python

import os

import sys
sys.setrecursionlimit(20000)


class NotHeader(Exception):
    pass


def generate(source_directory):
    all_functions = [f for l in get_all_functions(source_directory) for f in l]

    for function in all_functions:
        print(function)


def get_all_functions(source_directory):
    for file in get_source_files(source_directory):
        print("Getting from file %s" % file)
        yield get_functions_from_source(file)


def get_functions_from_source(file_name):
    with open(file_name, 'r', encoding="ISO-8859-1") as file:
        while True:
            try:
                function = get_function(get_character_generator(file))

                if function:
                    yield function

            except StopIteration:
                return


def get_function(file):
    def clear_to_new_line():
        character = next(file)

        if character != "\n":
            clear_to_new_line()

    def get_header():
        character = next(file)

        if character == "#":
            clear_to_new_line()
            raise NotHeader

        if character == ";":
            raise NotHeader

        if character == "{":
            return ""

        return character + get_header()

    def get_rest_of_block(bracket_depth=0):
        character = next(file)

        if character == "{":
            bracket_depth += 1

        if character == "}":
            if bracket_depth == 0:
                return ""
            else:
                bracket_depth -= 1

        return character + get_rest_of_block(bracket_depth)

    try:
        header = get_header()
    except NotHeader:
        return

    body = get_rest_of_block()

    print("Function with %d header and %d body" % (len(header), len(body)))

    return "%s{%s}" % (header, body)


def get_source_files(source_directory):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith(".h") or file.endswith(".c"):
                yield os.path.join(root, file)


def get_character_generator(file):
    for line in file:
        for character in line:
            yield character
