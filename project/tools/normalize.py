#!/usr/bin/env python

# mdstrip.py: makes new notebook from old, stripping md out

"""A tool to copy cell_type=("code") into a new file
without grabbing headers/markdown (most importantly the md)
NOTE: may want to grab the headers after all, or define new ones?"""

import os
import IPython.nbformat.current as nbf
from glob import glob
from lib import get_project_dir
import sys



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
    nbf.write(output_nb, out_file, "ipynb")


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
        sys.exit("Normalization error: '{}'".format(str(e)))