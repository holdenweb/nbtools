"""
sanity.py: Ensure the project structure's integrity is uncompromised.
"""
import os

from jinja2 import Environment, FileSystemLoader

def nullstrip(file):
    for line in file:
        if line.strip() and line[0] != "#":
            yield line
    
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

# Check all required notebooks exist
for tag in tags:
    filename = os.path.join("notebooks", tag+".ipynb")
    if not os.access(filename, os.R_OK):
        # Publication notebooks (which is what I had
        # in mind) will soon be automated by make,
        # as will other notebook types. All driven
        # by a scrupulously combed source. I hope.
        new_nb = open(filename, "w")
        nb_content = nb_template.render({"title": tag_names[tag],
                                         "date": "today",
                                         "time": "now"}) 
        new_nb.write(nb_content)
        new_nb.close()
        print("Created missing notebook", tag)
