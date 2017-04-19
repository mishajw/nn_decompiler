#!/usr/bin/env python

import argparse
import os
import re

word_regex = re.compile("\w+|[^\w\s]+")

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
parser.add_argument("--new_line_token", type=str, default="<newline>")

def main():
    args = parser.parse_args()

    all_words = []

    for file in os.listdir(args.input):
        path = os.path.join(args.input, file)

        if not os.path.isfile(path):
            continue

        with open(path, 'r') as f:
            all_words.append(parse_file(f, args.new_line_token))


def parse_file(f, new_line_token):
    for line in f:
        for word in word_regex.findall(line):
            yield word

        yield new_line_token



if __name__ == "__main__":
    main()

