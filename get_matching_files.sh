#!/usr/bin/env sh

# 1) Get all files in output
find output | \
# 2) Remove all /output, /cpp, /asm paths
# 3) Remove all .cpp and .asm extensions
    sed 's/\///g;s/^output//g;s/^cpp//g;s/^asm//g;s/.cpp$//g;s/.asm$//g;/^$/d' | \
# 4) Group lines with count
    sort | \
    uniq -c | \
# 5) Only print those that don't have a count of one
    grep -Ev "^ *1"
