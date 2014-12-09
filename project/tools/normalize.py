#!/usr/bin/env python

# normalize.py: makes new notebook from old, stripping out code cell
#               numbering and output cells

"""A tool to copy cell_type=("code") into a new file
without grabbing headers/markdown (most importantly the md)
NOTE: may want to grab the headers after all, or define new ones?"""

from glob import glob
import io
import simplejson as json
import os
import sys

import IPython.nbformat.current as nbf

from lib import get_project_dir

def normalize(in_file, out_file):
    worksheet = in_file.worksheets[0]
    cell_list = []
    # add graphic here & append to cell_list

    for cell in worksheet.cells:
        if cell.cell_type == ("code"):
            cell.outputs = []
            cell.prompt_number = ""
        cell_list.append(cell)
    output_nb = nbf.new_notebook() # XXX should set name ...
    output_nb.worksheets.append(nbf.new_worksheet(cells=cell_list))
    tmp_file = io.StringIO()
    nbf.write(output_nb, tmp_file, "ipynb")
    # Then write reorganized (i.e. key-sorted) JSON file to out_file
    tmp_file.seek(0)
    j_nb = json.load(tmp_file)
    json.dump(j_nb, out_file, sort_keys=True, indent=2)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        infile = open(sys.argv[1])
        outfile = open(sys.argv[2],"w")
    elif len(sys.argv) != 1:
        sys.exit("normalize: two arguments or none, please")
    else:
        infile = sys.stdin
        outfile = sys.stdout
    try:
        normalize(nbf.read(infile, "ipynb"), outfile)
    except Exception as e:
        print("Normalization error: '{}'".format(str(e)))
        sys.exit(-1)
