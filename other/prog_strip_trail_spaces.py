#!/bin/env python

# -*- coding: cp866 -*-

import os
import sys

assert len(sys.argv) > 1, "{0} filenames".format(sys.argv[0])

for filename in sys.argv[1:]:
    if not os.path.isfile(filename):
        continue

    with open(filename, "r", encoding = "cp866") as infile:
        data = [line.rstrip() + "\n" for line in infile]

    with open(filename, "w", encoding = "cp866") as outfile:
        [outfile.write(line) for line in data]
