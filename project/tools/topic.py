#!/usr/bin/env python
#
# topic.py
#
# Make a notebook for a new topic
#
from glob import glob
import os
import sys

import lib
from lib import nullstrip, slugify

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

def topic(words, exists=True):
    "Takes a list of words returning the topics that match"
    topic_words = [word.lower() for word in words]
    #print("Matching", topic_words)
    topics = get_topics()
    #print(len(topics))
    slugs = [slugify(topic.strip()) for topic in topics]
    for title, slug in zip(topics, slugs):
        title_words =  set([word.lower() for word in title.split()])
        #print(title_words)
        if all((word in title_words) for word in topic_words):        
            if os.path.isfile(os.path.join("nbsource", slug+".ipynb")) != exists:
                # If the topic exists do not overwrite it
                # XXX [unless option set]. Better comment required, or lose
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
    if len(sys.argv) > 1 and sys.argv[1][0] == "-":
        if sys.argv[1] == "-u":
            exists = True
        elif sys.argv[1] == "-o":
            orphaned = True
        elif sys.argv[1] == "-a":
            exists = None
        del sys.argv[1]
            
    if orphaned:
        orphaned_topic_files()
    else:
        topic(sys.argv[1:], exists=exists)