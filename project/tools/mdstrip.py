#!/usr/bin/env python

# mdstrip.py: makes new notebook from old, stripping md out

"""A tool to copy cell_type=("code") into a new file
without grabbing headers/markdown (most importantly the md)
NOTE: may want to grab the headers after all, or define new ones?"""

import os
import IPython.nbformat.current as nbf
from os.path import basename
from glob import glob
from lib import get_project_dir, nullstrip, slugify
import sys
import io

tools_dir = os.path.dirname(os.path.realpath(__file__))
title_data = open(os.path.join(tools_dir, "TitleBook.ipynb")).read()

def mdstrip(paths):
    for path in paths:

        if os.path.isdir(path):
            files = glob(os.path.join(path, "*.ipynb"))
        else:
            files = [path]
            
        for in_file in files:
            input_nb_name = basename(in_file)
            slug = input_nb_name[:-6]
            title = slug.replace("_", " ")
            actual_title_nb = io.StringIO(
                    title_data.replace("{{ title }}", title))
            title_nb = nbf.read(actual_title_nb, "ipynb")
            title_cell = title_nb.worksheets[0].cells[0]
            input_nb = nbf.read(open(in_file), "ipynb")
            worksheet = input_nb.worksheets[0]
            # add graphic here & append to cell_list
            cell_list = [title_cell]
            for cell in worksheet.cells:
                if cell.cell_type == ("code"):
                    cell.outputs = []
                    cell_list.append(cell)
                elif cell.cell_type == "heading":
                    cell_list.append(cell)
            output_nb = nbf.new_notebook()
            output_nb_name = slug+".prod.ipynb"
            output_nb.worksheets.append(nbf.new_worksheet(cells=cell_list))
            
            with open(output_nb_name, 'w') as f:
                nbf.write(output_nb, f, "ipynb")

if __name__ == "__main__":
    os.chdir(get_project_dir())
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = glob("*.ipynb")
    mdstrip(paths)
