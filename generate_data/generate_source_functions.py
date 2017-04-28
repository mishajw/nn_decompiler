#!/usr/bin/env python

import os
import re


class SourceFunction:
    def __init__(self, name, body):
        self.name = name
        self.body = body


class NotHeader(Exception):
    pass


def generate(source_directory):
    all_functions = get_all_functions(source_directory)

    for functions in all_functions:
        for function in functions:
            yield function


def get_all_functions(source_directory):
    for file in get_source_files(source_directory):
        yield get_functions_from_source(file)


def get_functions_from_source(file_name):
    with open(file_name, 'r', encoding="ISO-8859-1") as file:
        while True:
            try:
                function = get_function(get_commentless_generator(get_character_generator(file)))

                if function:
                    yield function

            except StopIteration:
                return

def clear_to_new_line(file):
    character = next(file)

    if character != "\n":
        clear_to_new_line(file)


def get_function(file):
    def get_header():
        character = next(file)

        if character == "#":
            clear_to_new_line(file)
            raise NotHeader

        if character == ";":
            raise NotHeader

        if character == "{":
            return ""

        return character + get_header()

    def get_rest_of_block(bracket_depth=0):
        for character in file:
            if character == "{":
                bracket_depth += 1

            if character == "}":
                if bracket_depth == 0:
                    return
                else:
                    bracket_depth -= 1

            yield character

    try:
        header = get_header()
    except NotHeader:
        return
    except RuntimeError as e:
        print("Error while reading header: %s" % e)
        return

    function_name = get_function_name(header)

    if not function_name:
        return

    body = "".join(get_rest_of_block())

    return SourceFunction(function_name, "%s{%s}" % (header, body))


def get_function_name(header):

    header_regex = re.search("^\s*.* ([0-9A-Za-z_]+)\(.*\)\s+$", header)

    if not header_regex:
        return

    return header_regex.group(1)


def get_source_files(source_directory):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith(".h") or file.endswith(".c"):
                yield os.path.join(root, file)


def get_character_generator(file):
    for line in file:
        for character in line:
            yield character


def clear_to_close_block(file, astrix_before = False):
    current_char = next(file)

    if current_char == "/" and astrix_before:
        print("end block")
        return
    elif current_char == "*":
        print("single astrix")
        clear_to_close_block(file, True)

    clear_to_close_block(file)


def get_commentless_generator(file, slash_before=False):
    current_char = next(file)
    print(current_char)

    if current_char == "/":
        if slash_before:
            print("double slash")
            clear_to_new_line(file)
            yield from get_commentless_generator(file)
        else:
            print("single slash")
            yield current_char
            yield from get_commentless_generator(file, True)
    elif current_char == "*" and slash_before:
        print("block")
        clear_to_close_block(file)
        yield from get_commentless_generator(file)
    else:
        yield current_char

