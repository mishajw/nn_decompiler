#!/usr/bin/env sh

# 1) Get all files in output
find output | \
# 2) Remove all /output, /c, /asm paths
# 3) Remove all .c and .asm extensions
    sed 's/\///g;s/^output//g;s/^c//g;s/^asm//g;s/.c$//g;s/.asm$//g;/^$/d' | \
# 4) Group lines with count
    sort | \
    uniq -c | \
# 5) Only print those that don't have a count of one
    grep -Ev "^ *1" |
# 6) Remove count
    sed 's/^\s\+[0-9]\+\s\+//g' 
