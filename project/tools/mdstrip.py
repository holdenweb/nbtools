#!/usr/bin/env python

# mdstrip.py: makes new notebook from old, stripping md out

"""A tool to copy cell_type=("code") into a new file
without grabbing headers/markdown (most importantly the md)
NOTE: may want to grab the headers after all, or define new ones?"""

import os
import IPython.nbformat.current as nbf
from os.path import basename # to strip off file extension before re-adding it :)
from glob import glob
from lib import get_project_dir, nullstrip, slugify
import sys


def mdstrip(paths):
    for path in paths:

        outline = nullstrip(open("outline.txt"))
        slug_dict = {}
        for line in outline:
            title = line.strip().rstrip(" *")
            slug = slugify(title)
            slug_dict[slug] = title

        if os.path.isdir(path):
            files = glob(os.path.join(path, "*.ipynb"))
        else:
            files = [path]
            
        for in_file in files:
            # print ("processing file:", in_file)
            input_nb = nbf.read(open(in_file), "ipynb")
            worksheet = input_nb.worksheets[0]
            input_nb_name = basename(in_file)
            slug = input_nb_name[:-6]
            if slug not in slug_dict:
                print("Missing slug:", slug)
                title = slug
            else:
                title = slug_dict[slug]
            source_lines = ["""## <img src="https://dl.dropboxusercontent.com/u/6117375/"""
                            """intermediate-notebooks/title_graphic.png" /> {}\n""".format(title)]
            cell_list = [nbf.new_text_cell(cell_type="markdown", source=source_lines)]
            # add graphic here & append to cell_list

            for cell in worksheet.cells:
                if cell.cell_type == ("code"):
                    cell.outputs = []
                    #cell.outputs = [{
                        #"metadata": {},
                        #"output_type": "pyout",
                        #"text": [""]
                    #}]                                                                                                                                                                                                                    
                    cell_list.append(cell)
            output_nb = nbf.new_notebook()
            # print (os.path.abspath(os.path.join("code_nbs", input_nb_name)))
            output_nb_name = os.path.join("code_nbs", input_nb_name)
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
