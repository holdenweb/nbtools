#!/usr/bin/env python
#
# topisc.py
#
# Make a notebook for a new topic
#
from glob import glob
import os
import sys

import lib
from lib import nullstrip, slugify, get_project_dir

# XXX Currently runs only from the project directory.
#     I am inclined to leave it that way for now
# template_env = Environment(loader=FileSystemLoader("data/templates"))
# -t template would be nice, but this will do for now
# src_template = template_env.get_template("base.ipynb")

def get_topics():
    topics = []
    for line in nullstrip(open("outline.txt")):
        topics.append(line.strip().rstrip(" *"))
    return topics

def topic_and_file(words, exists=True):
    """Takes a list of words returning the topics that match.
    
    exists: True, file must exist
            False, must not exist
            None: don't care."""
    search_words = [word.lower() for word in words]
    topics = get_topics()
    slugs = [slugify(topic.strip()) for topic in topics]
    for title, slug in zip(topics, slugs):
        title_words =  set([word.lower() for word in title.split()])
        if all((word in title_words) for word in search_words): 
            if (exists is None) or (os.path.exists(
                os.path.join("nbsource", slug+".ipynb")) != exists):
                print(title)

def orphaned_topic_files():
    topics = get_topics()
    slugs = [slugify(topic.strip()) for topic in topics]
    slug_topic = {slug: filename for (slug, filename) in zip(slugs, topics)}
    filenames = glob(os.path.join("nbsource", "*.ipynb"))
    file_slugs = [os.path.splitext(os.path.basename(f))[0] for f in filenames]
    for slug in file_slugs:
        if slug not in slugs:
            print(os.path.join("nbsource", slug+".ipynb"))

if __name__ == "__main__":
    # possible -d option for directory?
    exists = orphaned = False
    # XXX one switch only ... use proper arg parsing
    if len(sys.argv) > 1 and sys.argv[1][0] == "-":
        if sys.argv[1] == "-u":
            exists = True
        elif sys.argv[1] == "-o":
            orphaned = True
        elif sys.argv[1] == "-a":
            exists = None
        else:
            import sys
            sys.exit("topic.py [-d | -u | -a] [List of words]")
        del sys.argv[1]

    os.chdir(get_project_dir())

    if orphaned:
        orphaned_topic_files()
    else:
        topic_list = slugify(" ".join(sys.argv[1:])).split("-")
        if topic_list == [""]: # Annoying special case?
            topic_list = [] 
        topic_and_file(topic_list, exists=exists)