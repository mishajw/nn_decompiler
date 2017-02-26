#!/usr/bin/env python

import subprocess
import re
import sys


class AssemblyFunction:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines


def generate(object_file):
    process = subprocess.Popen(
        ["objdump", "-d", object_file],
        stdout=subprocess.PIPE)

    # Remove header of objdump output
    for i in range(6):
        next(process.stdout)

    while True:
        function = get_function(process.stdout)

        if function:
            print(function.name)

            for line in function.lines:
                print(line)


def get_function(object_dump):
    function_header_line = next(object_dump).rstrip().decode()

    function_header_regex = \
        re.search("^[0-9a-z]+ <([0-9A-Za-z_\.]+)>:", function_header_line)

    if not function_header_regex:
        sys.stderr.write("Couldn't find function header in %s\n" % function_header_line)
        return

    function_name = function_header_regex.group(1)

    def get_function_lines():
        for line in object_dump:
            if line.rstrip().decode() == "":
                return
            else:
                yield line.rstrip().decode()

    return AssemblyFunction(function_name, list(get_function_lines()))
