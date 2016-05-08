# -*- coding: utf-8 -*-

'''
    make.py -- build system
'''

import jinja2
import json

SRCFILE = os.path.join(__file__, 'src/index.html.template')
DESTFILE = 'index.html'
DATA = os.path.join(__file__, 'data/project.json')

def main():
    projects = json.load(open(DATA))
    template = open(SRCFILE).read()

    out = jinja2.Template(template).render({"projects": projects})
    open(DESTFILE, 'w').write(out)

    return 0
