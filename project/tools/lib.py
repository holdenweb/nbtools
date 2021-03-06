#
# lib.py: utility functions for the Notebook handlers
#
"""This file takes the difficulties out of working with directories,
and it also reduces clutter in at least one program."""

import os

def get_project_dir(default="."):
    return os.environ.get("SCAM_PROJECT", default)

def newer(file1, file2):
    file1_modification = os.stat(file1).st_mtime
    file2_modification = os.stat(file2).st_mtime
    return file1_modification > file2_modification

def nullstrip(file):
    for line in file:
        if line.rstrip() and line[0] != "#":
            yield line

def slugify(title):
    for char in ("!?:.,*"):
        title = title.replace(char, "")
    title = title.strip()
    return title.replace(" - ", "-").replace(" ", "-").lower()