"""
sanity.py: Ensure the project structure's integrity is uncompromised.
"""
import datetime
import os

import IPython.nbformat.current as nbf

from jinja2 import Environment, FileSystemLoader

def nullstrip(file):
    for line in file:
        if line.strip() and line[0] != "#":
            yield line

def newer(file1, file2):
    file1_creation = os.stat(file1).st_ctime
    file2_creation = os.stat(files).st_ctime
    return file1_creation > file2_creation

# Load configuration data from outline (currently just a list of topics)
names = [line.strip().rstrip(" *")
         for line in nullstrip(open("outline.txt", "r"))]
tags = [name.replace(".", "").replace(" ", "-").lower() for name in names]
tag_names = dict(zip(tags, names))

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

root = Directory(".")
# Establish jinja templating environment
jenv = Environment(loader=FileSystemLoader("data/templates"))
nb_template = jenv.get_template("base.ipynb")

# Check all required notebook sources exist
# (and regenerate them if their source notebook
# is newer than the target - make is on the horizon
for tag in tags:
    now = datetime.datetime.today()
    nb_name = tag+".ipynb"
    src_file = os.path.join("nbsource", nb_name)
    dest_file = os.path.join("notebooks", nb_name)
    try:
    except FileNotFoundError:
        print ("Missing source:", src_file)
        continue
    # The cells in the template are copied across
    # unless they contain processing instructions.
    # We currently assume that none do, and treat
    # and empty cell as needing to be replaced with
    # the cells from the source notebook.
    # Ultimately this will be handled by pragmas.
    if not (os.access(src_file, os.R_OK) or
            newer(src_file, dest_file)):
        # Publication notebooks (which is what I had
        # in mind) will soon be automated by make,
        # as will other notebook types. All driven
        # by a scrupulously combed source. I hope.
        # For now, let's just be happy with what we have.
        new_nb = open(dest_file, "w")
        nb_content = nb_template.render({"slug": tag,
                                         "title": tag_names[tag],
                                         "date": now.date(),
                                         "time": now.time(),
                                         "src_file": src_file}) 
        new_nb.write(nb_content)
        new_nb.close()
        # Now we've done the easy stuff (templating)
        # we read in the newly-created notebook and
        # manipulate its structure according to the
        # pragmas found in the various cells.
        
        print("Created notebook", tag)
