#!/usr/bin/env python3

import sys

not_printed = True
head = []

for line in sys.stdin:
    line = line.strip()
    a = line.split()
    if "_rln" in line:
        head.append(line.split("_rln")[1])
    elif len(a) > 3 and any(c.isalnum() for c in line):
        if not_printed:
            print("\t".join(head))
            not_printed = False
        print(line)


# This Python code performs the same functionality as the original Perl script:
#
# 1. It reads input from standard input (`sys.stdin` in Python).
# 2. It splits each line into elements using whitespace as the delimiter.
# 3. It checks if the line contains "_rln" and extracts the relevant part to populate the `head` list.
# 4. If the line does not contain "_rln" and has more than 3 elements and at least one alphanumeric character, it prints
# the line after printing the header if it hasn't been printed yet.
#
# Make sure to replace the functionality in `sys.stdin` with actual input data or pipe input from a file when running the
# Python script.
