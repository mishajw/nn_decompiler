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
            yield function


def get_function(object_dump):
    function_header_line = next(object_dump).rstrip().decode()

    function_header_regex = \
        re.search("^[0-9a-z]+ <([0-9A-Za-z_\.]+)>:", function_header_line)

    if not function_header_regex:
        sys.stderr.write("Couldn't find function header in %s\n" % function_header_line)
        return

    function_name = function_header_regex.group(1)

    def parse_function_line(line):
        line_regex = re.search("^\s+[0-9a-f]+:\s+([0-9a-f]{2}\s)*[0-9a-f]{2}\s\s+(.*)", line)

        if line_regex:
            return line_regex.group(2)
        else:
            return

    def get_function_lines():
        for line in object_dump:
            if line.rstrip().decode() == "":
                return

            parsed_line = parse_function_line(line.rstrip().decode())

            if parsed_line:
                yield parsed_line

    return AssemblyFunction(function_name, list(get_function_lines()))
