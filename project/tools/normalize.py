#!/usr/bin/env python

# mdstrip.py: makes new notebook from old, stripping md out

"""A tool to copy cell_type=("code") into a new file
without grabbing headers/markdown (most importantly the md)
NOTE: may want to grab the headers after all, or define new ones?"""

import os
import IPython.nbformat.current as nbf
from os.path import basename # to strip off file extension before re-adding it :)
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

    output_nb.worksheets.append(nbf.new_worksheet(cells=cell_list))
    

if __name__ == "__main__":
    os.chdir(get_project_dir())
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = glob("*.ipynb")
    for input_nb_name in paths:
        # print ("processing file:", in_file)
        input_nb = nbf.read(open(input_nb_name), "ipynb")
        output_nb = nbf.new_notebook()
        output_nb_name = input_nb_name[:-6]+".min.ipynb"
        normalize(input_nb, output_nb)
        with open(output_nb_name, 'w') as f:
            nbf.write(output_nb, f, "ipynb")
