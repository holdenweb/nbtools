#!/usr/bin/env python
#
# nbstats.py: report some statistics on a collection of notebooks
#
"""\
If no arguments are provided then all notebook files in the "nbsource"
subdirectory of the project directory (determined by accessing the
SCAM_PROJECT environment variable if it exists, otherwise the current 
directory).

If a directory is passed as a single argument then all ".ipynb" files
in that directory are processed. Otherwise all arguments are
processed as notebook files. 

The program provides information about the content that will
hopefully give a useful measure of content growth as time passes by."""

import os
import sys
from collections import defaultdict
from glob import glob

import IPython.nbformat.current as nbf
from lib import get_project_dir

def nbstats(paths):
    results = []
    for path in paths:
        if os.path.isdir(path):
            files = glob(os.path.join(path, "*.ipynb"))
        else:
            files = [path]
        for in_file in files:
            notebook = nbf.read(open(in_file), "ipynb")
            filename = os.path.basename(in_file)
            code_lines = code_bytes = doc_lines = doc_bytes = 0
            worksheet = notebook.worksheets[0]
            cell_count = len(worksheet.cells)
            cell_type_count = defaultdict(int)
            if cell_count > 1:
                for cell in worksheet.cells:
                    cell_type = cell.cell_type
                    cell_type_count[cell_type] += 1
                    if cell_type in ("markdown", "code"):
                        if cell_type == "markdown":
                            source = cell.source.splitlines()
                            lines, bytes = get_lines_and_bytes(source)
                            doc_lines += lines
                            doc_bytes += bytes
                        else:
                            source = cell.input.splitlines()
                            lines, bytes = get_lines_and_bytes(source)
                            code_lines += lines
                            code_bytes += bytes
                results.append((in_file, cell_type_count["code"], code_lines,
                                code_bytes, cell_type_count["markdown"],
                                doc_lines, doc_bytes))
    if results:
        longest = max(len(r[0]) for r in results)-6 # == len(".ipynb")
    else:
        sys.exit("No notebooks with more than one cell")
    
    totals = [0, 0, 0, 0, 0, 0]
    format_str = "{:>{length}} {:4d} {:6,d} {:6,d} {:4d} {:6,d} {:6,d}"
    format_hdr = "{:>{length}} {}"
    print(format_hdr.format("", "------ code ------ ---- markdown ----", length=longest))
    print(format_hdr.format("", "cells  lines chars cells  lines chars", length=longest))
    for result in results:
        result = list(result)
        result[0] = result[0][:-6]
        totals = [total+count for (total, count) in zip(totals, result[1:])]
        print(format_str.
              format(*result, length=longest))
    print(format_str.format(*["TOTALS"]+totals, length=longest))

def get_lines_and_bytes(source):
    lines = sum(l != "\n" for l in source)
    bytes = sum(len(l) for l in source)
    return lines, bytes

if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.chdir(os.path.join(get_project_dir(), "nbsource"))
        paths = glob("*.ipynb")
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        os.chdir(sys.argv[1])
        paths = glob("*.ipynb")
    else:
        paths = sys.argv[1:]
    nbstats(paths)
    