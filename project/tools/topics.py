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

def matching(word, title_words):
    # The empty word is always present
    if not len(word):
        return True
    return any(word in tword for tword in title_words)

def get_topics():
    topics = []
    for line in nullstrip(open("outline.txt")):
        line = line.rstrip().rstrip(" *")
        sline = line.lstrip()
        topics.append((sline, len(line)-len(sline)))
    return topics

def topic_and_file(words, exists=True):
    """Takes a list of words returning the topics that match.
    
    exists: True, file must exist
            False, must not exist
            None: don't care."""
    search_words = [word.lower() for word in words]
    topics = get_topics()
    slugs = [slugify(topic[0].strip()) for topic in topics]
    for (title, indent), slug in zip(topics, slugs):
        title_words =  set([word.lower() for word in title.split()])
        if all(matching(word, title_words) for word in search_words):
            if (exists is None) or (os.path.exists(
                os.path.join("project", "nbsource", slug+".ipynb")) != exists):
                print(" "*indent+title)

def orphaned_topic_files():
    topics = get_topics()
    slugs = [slugify(topic[0].strip()) for topic in topics]
    filenames = glob(os.path.join("nbsource", "*.ipynb"))
    file_slugs = [os.path.splitext(os.path.basename(f))[0] for f in filenames]
    for slug in slugs:
        comment = " ***" if slug not in file_slugs else ""
        print(os.path.join("project", "nbsource", slug+'.ipynb'), comment)

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
            sys.exit("topics.py [-o | -u | -a] [List of words]")
        del sys.argv[1]

    os.chdir(get_project_dir())

    if orphaned:
        orphaned_topic_files()
    else:
        topic_list = slugify(" ".join(sys.argv[1:])).split("-")
#        if topic_list == [""]: # Annoying special case?
#            topic_list = [] 
        topic_and_file(topic_list, exists=exists)