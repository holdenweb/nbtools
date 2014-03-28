#!/usr/bin/env python
"""
extract.py: Sends notebook content to the standard output
"""
import datetime
import os
import shutil
import sys
from glob import glob

import IPython.nbformat.current as nbf

from jinja2 import Environment, FileSystemLoader
from lib import newer, nullstrip, slugify, get_project_dir

def main():
    os.chdir(get_project_dir())
    cell_types = set()
    args = sys.argv[1:]
    # XXX if both code and markdown should indent code 4 spaces as emitted
    while args and args[0].startswith("-"):
        arg = args[0]
        del args[0]
        if arg=="-c":
            cell_types.add("code")
        elif arg=="-m":
            cell_types.add("markdown")
        elif arg=="-h":
            cell_types.add("heading")
        else:
            sys.exit("Usage: extract.py [-c] [-m] [-h] filename ...")
    
    for src_file in args:
        # Establish jinja templating environment (Do we even need to render?)
        #template_env = Environment(loader=FileSystemLoader("data/templates"))
        #src_template = template_env.get_template("markdown-only.ipynb")
        now = datetime.datetime.today()
        render_context = {"title": "Markdown extracted from "+os.path.abspath(src_file),
                          "date": now.date(),
                          "time": now.time(),
                          "src_file": src_file,
                          "template": "UNKNOWN"}
        # All cells of the chosen type in the source notebook are copied across.
        text_out = sys.stdout
        src_nb = nbf.read(open(src_file, "r", encoding="UTF-8"), "ipynb")
        # At present we don't render the extracted
        # cell content, but that possibility remains open.
        for worksheet in src_nb.worksheets:
            cells_in = worksheet.cells
            for cell in cells_in:
                if cell.cell_type in cell_types:
                    if cell.cell_type == "code":
                        if "markdown" not in cell_types:
                            text_out.write(cell.input)
                        else:
                            text_out.write("".join("    "+line for line in cell.input.splitlines(keepends=True)))
                    elif cell.cell_type == "markdown":
                        text_out.write(cell.source)
                    elif cell.cell_type == "heading":
                        text_out.write("{} {}\n".format(
                            "#"*cell.level, cell.source))
                    else:
                        sys.exit("Should not have been called to process %s cells",
                                 cell.cell_type)
                    text_out.write("\n\n")
        text_out.close()

if __name__ == "__main__":
    main()