#!/usr/bin/env python

# mdstrip.py: makes new notebook from old, stripping md out

"""A tool to copy cell_type=("code") into a new file
without grabbing headers/markdown (most importantly the md)
NOTE: may want to grab the headers after all, or define new ones?"""

import os
import sys # for sys.argv
import IPython.nbformat.current as nbf
import datetime
from os.path import basename # to strip off file extension before re-adding it :)
from glob import glob
from lib import get_project_dir, slugify
from shutil import copyfileobj # to copy pieces
from mktopic import mktopic # to make new nb

def mdstrip(paths):
	for path in paths:
		if os.path.isdir(path):
           	files = glob(os.path.join(path, "*.ipynb"))
		else:
            files = [path]
        for in_file in files:
           	input_nb = nbf(open(in_file), "ipynb")
           	worksheet = input_nb.worksheets[0]
           	print "the file you're working with is: %s" % input_nb
        	input_nb_name = basename(in_file) # will this work since we set var to entire
        								 # filename, not file.ipynb?
            # read CELLS rather than lines - will be same?
            # first to make new notebook
            # read nb & make list of all code cells
            cell_list = []
            for cell in worksheet.cells:
            	# cell counting mechanism here to tell how many are ported into new .ipynb file?
                   	if cell_type == ("code"):
               			cell_list.append(cell)

                   		# first to make new notebook
                   		# then to write every cell that meets cell_type=("code") to new nb
                   		# should this be a list of all relevant cells?

            			# now copy contents equalling
        				# source_content = txt_file.read()
        				# dst_file.write(source_content)
        				# print "source_content of %s has been written to " % imported_nb
    				else:
    					break # do nothing for header/markdown
    						  # note: may want to do something for single md cell with logo & name.
	  		output_nb = nbf.new_notebook()
	  		output_nb_name = os.path.join("code_nbs", input_nb_name)
	  		output_nb.worksheets.append(nbf.new_worksheet(cells=cell_list))
	  		with open(output_nb_name, 'w') as f:
	  			nbf.write(output_nb, f, "ipynb")

if __name__ == "__main__":
    os.chdir(os.path.join(get_project_dir(), "nbsource"))
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = glob("*.ipynb")
    mdstrip(paths)