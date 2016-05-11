# -*- coding: utf-8 -*-

'''
    build system
'''

import os
import sys
import json

import jinja2

DIR = os.path.dirname(__file__)
SRCFILE = os.path.join(DIR, 'templates/index.template')
DESTFILE = 'index.html'
DATA = os.path.join(DIR, 'data/project.json')
CONFIG_FILE = os.path.join(DIR, 'build.conf.json')


def main():
#    config = json.load(open(CONFIG_FILE))
#    gh_projects = gh_project(config['gh-name'])
#    projects = json.load(open(DATA))
#    template = open(SRCFILE).read()
#
#    out = jinja2.Template(template).render({"projects": projects})
#    open(DESTFILE, 'w').write(out)
    config = json.load(open(CONFIG_FILE))
    projects = gh_projects(config['gh-name'])
    print projects

    return 0
