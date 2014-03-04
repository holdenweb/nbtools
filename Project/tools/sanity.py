"""
sanity.py: Ensure the project structure's integrity is uncompromised.
"""
import json
import datetime
import os
import shutil

import IPython.nbformat.current as nbf

from jinja2 import Environment, FileSystemLoader
from lib import newer, nullstrip

# Filestore tree representation (for faster inferencing)
class Directory:
    """Represent a directory with a list of files and subdirectories."""
    def __init__(self, dir):
        self.root , self.dirs, self.files = next(os.walk(dir))
    def enumerate(self):
        for dir, subdirs, files in walker:
            print("\nDirectory:", dir())
            for file in files:  
                print(file)

root = Directory(".") # may be redundant for now.
# Load configuration data from outline (currently just a list of topics)
names = [line.strip().rstrip(" *")
         for line in nullstrip(open("outline.txt", "r"))]
tags = [name.replace(".", "").replace(" ", "-").lower() for name in names]
tag_names = dict(zip(tags, names))

# Establish jinja templating environment
jenv = Environment(loader=FileSystemLoader("data/templates"))
nb_template = jenv.get_template("base.ipynb")

# Check all required notebook sources exist
# (and regenerate them if their source notebook
# is newer than the target - make is on the horizon).
# This code should be migrated away from sanity.py.
for tag in tags:
    now = datetime.datetime.today()
    nb_name = tag+".ipynb"
    src_file = os.path.join("nbsource", nb_name)
    dst_file = os.path.join("notebooks", nb_name)
    if not os.path.isfile(src_file):
        # at this point the program should create a new stub source
        # notebook, but at present there is no recipe for doing so.
        print("Missing source for", tag_names[tag])
        continue # Should create stub source book
    # The cells in the template are copied across
    # unless they contain processing instructions.
    # Ultimately this will be handled by pragmas.
    if (not os.path.isfile(dst_file) or
            newer(src_file, dst_file)):
        # Publication notebooks (which is what I had
        # in mind) will soon be automated by make,
        # as will other notebook types. All driven
        # by a scrupulously combed source. I hope.
        # For now, let's just be happy with what we have.
        dst_nb_file = open(dst_file, "w")
        nb_content = nb_template.render({"slug": tag,
                                         "title": tag_names[tag],
                                         "date": now.date(),
                                         "time": now.time(),
                                         "src_file": src_file}) 
        dst_nb_file.write(nb_content)
        dst_nb_file.close()
        # Now we've done the easy stuff (templating)
        # we read in the newly-created notebook and
        # manipulate its structure according to the
        # pragmas found in the various cells.
        dst_nb = nbf.read(open(dst_file, 'r'), "ipynb")
        dst_worksheets = dst_nb.worksheets
        for wsno, worksheet in enumerate(dst_worksheets):
            cells_in = worksheet.cells
            cells_out = []
            for cell in cells_in:
                print(cell.source)
                if (cell.cell_type == "raw" 
                    and cell.source.startswith("#!cells")):
                    args = cell.source.split()[1:] # brittle#
                    # Nasty exception to this one (IPython.nbformat.current.NotJSONError)
                    # if the notebook is not conformant.
                    param_nb = nbf.read(open(args[0], "r"), "ipynb")
                    for pcell in param_nb.worksheets[wsno].cells:
                        cells_out.append(pcell)
                else:
                    cells_out.append(cell)
            worksheet.cells = cells_out
        outf = open(dst_file, 'w')
        nbf.write(dst_nb, outf, "ipynb")
        outf.close()
        print("Created notebook", tag)
