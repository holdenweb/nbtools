#!/usr/bin/env python
#
# nbrstats.py: report some statistics on a collection of notebooks
#
"""\
This program reads all the notebooks whose names are passed as arguments
(or if no arguments are given, all ".ipynb" files in the current 
directory) and provides information about the content that will
hopefully give a useful measure of content growth as time passes by."""

import os
import sys
from collections import defaultdict
from glob import glob

import IPython.nbformat.current as nbf

if len(sys.argv) > 1:
    paths = sys.argv[1:]
else:
    paths = glob("nbsource/*.ipynb")

results = []
for path in paths:
    notebook = nbf.read(open(path), "ipynb")
    filename = os.path.basename(path)
    code_lines = code_bytes = doc_lines = doc_bytes = 0
    worksheet = notebook.worksheets[0]
    cell_count = len(worksheet.cells)
    #print(path, cell_count)
    cell_type_count = defaultdict(int)
    if cell_count > 1:
        for cell in worksheet.cells:
            cell_type = cell.cell_type
            cell_type_count[cell_type] += 1
            if cell_type == "heading":
                cell_type = "heading"+str(cell["level"])
            if cell_type == "markdown":
                source = cell.source.splitlines()
                lines = sum(l != "\n" for l in source)
                bytes = sum(len(l) for l in source)
                doc_lines += lines
                doc_bytes += bytes
            elif cell_type == "code":
                source = cell.input.splitlines()
                lines = sum(l != "\n" for l in source)
                bytes = sum(len(l) for l in source)
                code_lines += lines
                code_bytes += bytes
        results.append((path, cell_type_count["code"], code_lines,
                        code_bytes, cell_type_count["markdown"],
                        doc_lines, doc_bytes))
if results:
    longest = max(len(r[0]) for r in results)
else:
    sys.exit("No files with more than one cell")

totals = [0, 0, 0, 0, 0, 0]
format_str = "{:>{length}} {:3d} {:5,d} {:6,d} {:3d} {:5,d} {:6,d}"
for result in results:
    totals = [total+count for (total, count) in zip(totals, result[1:])]
    print(format_str.
          format(*result, length=longest))
print(format_str.format(*["TOTALS"]+totals, length=longest))