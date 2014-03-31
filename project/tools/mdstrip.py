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

worksheet = notebook.worksheets[0] # this should probably go elsewhere

def mdstrip(paths):
	for path in paths:
		if os.path.isdir(path):
           	files = glob(os.path.join(path, "*.ipynb"))
		else:
            files = [path]
        for in_file in files:
           	input_nb = nbf(open(in_file), "ipynb")
           	print "the file you're working with is: %s" % input_nb
        	imported_nb = basename(in_file) # will this work since we set var to entire
        								 # filename, not file.ipynb?
            # read CELLS rather than lines - will be same?
            for cell in worksheet.cells:
            	# cell counting mechanism here to tell how many are ported into new .ipynb file?
                   	if cell_type in ("code"):
                   		# first to make new notebook via base ipynb template
                   		# then to write every cell that meets cell_type=("code") to new nb
                   		# should this be a list of all relevant cells?
                   		# # # ALLLLL this stuff: src_template,now,dst_file,
                   		# # # & render_context is just to make a new nb
                   		# 
                   		# also are these labels relevant when importing them?  title slug etc?
            			src_template = template_env.get_template("base.ipynb") 
            			# not sure if is steve's base or ipython's
						now = datetime.datetime.today()
				    	new_nb = open(imported_nb+"-minus-md.ipynb", 'w+') #e.g. tuples-minus-mid.ipynb
				    	dst_file = os.path.join("mdless_nbs", new_nb) # think this just puts it in dir
				    	render_context = {"slug": slug, # no longer have slug, just new_nb
                    		"title": title, # how will this be generated
                    		"date": now.date(),
                    		"time": now.time(),
                    		"src_file": new_nb,
                    		"template": src_template.filename} # stevenote: we are writing a source ...
            			# now copy contents equalling
        				# source_content = txt_file.read()
        				# dst_file.write(source_content)
        				# print "source_content of %s has been written to " % imported_nb
    				else:
    					break # do nothing for header/markdown
    						  # note: may want to do something for single md cell with logo & name.
    if os.path.isfile(dst_file):
        # If the topic exists do not overwrite it XXX [unless option set].
        sys.exit("file {} already exists".format(dst_file))

if __name__ == "__main__":
    os.chdir(os.path.join(get_project_dir(), "nbsource"))
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = glob("*.ipynb")
    mdstrip(paths)