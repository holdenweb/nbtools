#!/usr/bin/env python
#
# topic.py
#
# Make a notebook for a new topic
#
import os
import sys

import lib
from lib import nullstrip, slugify

# XXX Currently runs only from the project directory.
#     I am inclined to leave it that way for now
# template_env = Environment(loader=FileSystemLoader("data/templates"))
# -t template would be nice, but this will do for now
# src_template = template_env.get_template("base.ipynb")

def topic(words, exists=True):
    "Takes a list of words returning the topics that match"
    topic_words = [word.lower() for word in words]
    slugs = []
    topics = []
    for line in nullstrip(open("outline.txt")):
        line = line.strip().rstrip(" *")
        topics.append(line)
        slug = slugify(line.strip())
        slugs.append(slug)
        line_words =  set([word.lower() for word in line.split()])
        if all((word in line_words) for word in topic_words):        
            if os.path.isfile(os.path.join("nbsource", slug+".ipynb")) != exists:
                # If the topic exists do not overwrite it XXX [unless option set]. Better comment required, or lose
                print(line)

if __name__ == "__main__":
    # possible -d option for directory?
    exists = len(sys.argv) > 1 and sys.argv[1] == "-u"
    if exists:
        del sys.argv[1]
    topic(sys.argv[1:], exists=exists)