#
# lib.py: utility functions for the Motebopok handlers
#
"""This file takes the difficulties out of working with directories,
and it also reduces clutter in at least one program."""

import os

def newer(file1, file2):
    file1_creation = os.stat(file1).st_mtime
    file2_creation = os.stat(file2).st_mtime
    return file1_creation > file2_creation

def nullstrip(file):
    for line in file:
        if line.rstrip() and line[0] != "#":
            yield line

