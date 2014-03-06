"""
sanity.py: Ensure the project structure's integrity is uncompromised.
"""
from collections import namedtuple
import datetime
import os
import shutil
import sys

import IPython.nbformat.current as nbf

from jinja2 import Environment, FileSystemLoader
from lib import newer, nullstrip

Snippet = namedtuple("Snippet", "title slug indent_level section snippets")

wanted_cell_types = {"code", "markdown", "heading"}
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
root_snippet = Snippet(title="O'Reilly Media: Intermediate Python",
                       slug="SOMETHING MEANINGFUL AT A SYSTEM LEVEL",
                       indent_level=0, section=None, snippets=[])
slug_snippets = {}
indent_stack = [0]
snippet_stack = [root_snippet]
last_snippet  = root_snippet
slug_list = []
snippet_list = []
top_level_snippets = []
for line in nullstrip(open("outline.txt", "r")):
    assert len(snippet_stack), "Nothing on the stack!"
    title = line.strip().rstrip(" *")
    indent = (len(line)-len(line.lstrip()))
    if indent > indent_stack[-1]: # Lower level than previous
        indent_stack.append(indent)
        snippet_stack.append(last_snippet)
    while indent < indent_stack[-1]:
        indent_stack.pop()
        snippet_stack.pop()
        if indent > indent_stack[-1]:
            sys.exit("Mismatched indentation on", title)
    slug = title.replace(".", "").replace(" ", "-").lower()
    snippet = Snippet(title=title, slug=slug, indent_level=len(indent_stack),
                      section=False, snippets=[])
    slug_snippets[slug] = snippet
    snippet_stack[-1].snippets.append(snippet)
    slug_list.append(slug)
    snippet_list.append(snippet)
    if snippet.indent_level == 1:
        top_level_snippets.append(snippet)
    last_snippet = snippet

# Establish jinja templating environment
template_env = Environment(loader=FileSystemLoader("data/templates"))
nb_template = template_env.get_template("base.ipynb")
src_template = template_env.get_template("source_base.ipynb")

# Check all required notebook sources exist.
# XXX Check no spurious source files exist
# Regenerate them if their source notebook
# is newer than the target - make is on the horizon.
# This code should be migrated away from sanity.py.
for slug in slug_list:
    now = datetime.datetime.today()
    nb_name = slug+".ipynb"
    src_file = os.path.join("nbsource", nb_name)
    dst_file = os.path.join("notebooks", nb_name)
    render_context = {"slug": slug,
                      "title": slug_snippets[slug].title,
                      "date": now.date(),
                      "time": now.time(),
                      "src_file": src_file}
    if not os.path.isfile(src_file):
        # at this point the program should create a new stub source
        # notebook, but at present there is no recipe for doing so.
        src_content = src_template.render(render_context)
        open(src_file, "w").write(src_content)

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
        nb_content = nb_template.render(render_context) 
        dst_nb_file.write(nb_content)
        dst_nb_file.close()
        # Now we've done the easy stuff (rendering the template)
        # we read in the newly-created notebook and
        # manipulate its structure according to the
        # pragmas found in the various cells.
        # Right now there's just one pragma (#!cells)
        # that says "put all that shit in here".
        dst_nb = nbf.read(open(dst_file, 'r'), "ipynb")
        dst_worksheets = dst_nb.worksheets
        for wsno, worksheet in enumerate(dst_worksheets):
            cells_in = worksheet.cells
            cells_out = []
            for cell in cells_in:
                if (cell.cell_type == "raw" 
                    and cell.source.startswith("#!cells")):
                    args = cell.source.split()[1:] # brittle#
                    # Nasty exception to this one
                    # (IPython.nbformat.current.NotJSONError)
                    # if the notebook is not conformant.
                    param_nb = nbf.read(open(args[0], "r"), "ipynb")
                    for pcell in param_nb.worksheets[wsno].cells:
                        if pcell.cell_type in wanted_cell_types:
                                cells_out.append(pcell)
                        else:
                            print("%%% ignored cell type", pcell.cell_type)
                else: # copy other template cells to output
                    cells_out.append(cell)
            worksheet.cells = cells_out
        outf = open(dst_file, 'w')
        nbf.write(dst_nb, outf, "ipynb")
        outf.close()
        print("Built output notebook", slug)
print("Done")
