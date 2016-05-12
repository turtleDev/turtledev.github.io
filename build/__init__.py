# -*- coding: utf-8 -*-

'''
    build system
'''

import os
import sys
import json
import logging

import jinja2

from projects import gh_projects
from pages import pages

logging.basicConfig(level=logging.WARN,
                    format="%(asctime)s [%(name)s:%(lineno)d] %(levelname)s: %(message)s")

DIR = os.path.dirname(__file__)
SRCFILE = os.path.join(DIR, 'templates/index.template')
DESTFILE = 'index.html'
OTHER_PROJECTS = os.path.join(DIR, 'data/project.json')
CONFIG_FILE = os.path.join(DIR, 'build.conf.json')
PAGES_DIR = os.path.join(DIR, 'pages')


def main():
    template = open(SRCFILE).read()
    projects = []
    out = jinja2.Template(template).render({"projects": projects,
                                            "pages": pages(PAGES_DIR)})
    open(DESTFILE, 'w').write(out)

    return 0
