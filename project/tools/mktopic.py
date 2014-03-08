#!/usr/bin/env python
#
# mk_topic.py
#
# Make a notebook for a new topic
#
import datetime
import os
import sys

import lib
from jinja2 import Environment, FileSystemLoader
from lib import nullstrip, slugify

# XXX Currently runs only from the project directory.
#     I am inclined to leave it that way for now
template_env = Environment(loader=FileSystemLoader("data/templates"))
# -t template would be nice, but this will do for now
src_template = template_env.get_template("base.ipynb")

def mktopic(title):
    "Takes a list of the words of a topic title and builds the appropriate notebook file."
    now = datetime.datetime.today()
    title = " ".join(title)
    slug = lib.slugify(title)
    nb_name = slug+".ipynb"
    dst_file = os.path.join("nbsource", nb_name)
    render_context = {"slug": slug,
                      "title": title,
                      "date": now.date(),
                      "time": now.time(),
                      "src_file": dst_file,
                      "template": src_template.filename} # we are writing a source ...
    if os.path.isfile(dst_file):
        # If the topic exists do not overwrite it XXX [unless option set].
        sys.exit("file {} already exists".format(dst_file))
    dst_nb_file = open(dst_file, "w")
    nb_content = src_template.render(render_context) 
    dst_nb_file.write(nb_content)
    dst_nb_file.close()

if __name__ == "__main__":
    # possible -d option for directory?
    if len(sys.argv) < 2:
        sys.exit("Sorry, I need a topic name - just one!")
    mktopic(sys.argv[1:])