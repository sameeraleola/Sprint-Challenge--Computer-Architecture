#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# print(len(sys.argv))
# print(sys.argv[1])
try:
    f = open(sys.argv[1])
    f.close()
    cpu.load(sys.argv[1])
    cpu.run()
except IOError:
    print(f'Can not find program file: {sys.argv[1]}')