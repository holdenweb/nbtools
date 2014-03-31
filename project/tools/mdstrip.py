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
from lib import get_project_dir

worksheet = notebook.worksheets[0] # this should probably go elsewhere

def mdstrip(paths)
	for path in paths:
		if os.path.isdir(path):
           	files = glob(os.path.join(path, "*.ipynb"))
		else:
            files = [path]
        for in_file in files:
           	input_nb = nbf(open(in_file), "ipynb")
        	importednb = basename(in_file) # will this work since we set var to entire
        								 # filename, not file.ipynb?
            # read CELLS rather than lines - will be same?
            for cell in worksheet.cells:
            	# cell counting mechanism here to tell how many are ported into new .ipynb file?
                   	if cell_type in ("code"):
                   		# # # ALLLLL this stuff: src_template,now,new_nb,dst_file,
                   		# # # & render_context is just to make a new nb
            			src_template = template_env.get_template("base.ipynb") 
            			# not sure if is steve's base or ipython's
						now = datetime.datetime.today()
				    	new_nb = open(oldnb+"-minus-md.ipynb") #e.g. tuples-minus-mid.ipynb
				    	dst_file = os.path.join("nbsource", new_nb)
				    	render_context = {"slug": slug, # no longer have slug, just new_nb
                    		"title": title,
                    		"date": now.date(),
                    		"time": now.time(),
                    		"src_file": dst_file,
                    		"template": src_template.filename} # stevenote: we are writing a source ...
            			# now copy contents equalling 
    				else:
    					break # do nothing for header/markdown
    						  # note: may want to do something for header.
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