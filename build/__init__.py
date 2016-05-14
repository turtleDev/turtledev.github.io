# -*- coding: utf-8 -*-

'''
    build system
'''

import os
import sys
import json
import logging

import jinja2

from projects import projects
from pages import pages

logging.basicConfig(level=logging.WARN,
                    format="%(asctime)s [%(name)s:%(lineno)d] %(levelname)s: %(message)s")

DIR = os.path.dirname(__file__)
SRCFILE = os.path.join(DIR, 'templates/index.template')
DESTFILE = 'index.html'
OTHER_PROJECTS = os.path.join(DIR, 'data/project.json')
CONFIG_FILE = os.path.join(DIR, 'build.conf.json')
PAGES_DIR = os.path.join(DIR, 'pages')


ICONS = {'fork': 'viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg"><path d="M672 1472q0-40-28-68t-68-28-68 28-28 68 28 68 68 28 68-28 28-68zm0-1152q0-40-28-68t-68-28-68 28-28 68 28 68 68 28 68-28 28-68zm640 128q0-40-28-68t-68-28-68 28-28 68 28 68 68 28 68-28 28-68zm96 0q0 52-26 96.5t-70 69.5q-2 287-226 414-68 38-203 81-128 40-169.5 71t-41.5 100v26q44 25 70 69.5t26 96.5q0 80-56 136t-136 56-136-56-56-136q0-52 26-96.5t70-69.5v-820q-44-25-70-69.5t-26-96.5q0-80 56-136t136-56 136 56 56 136q0 52-26 96.5t-70 69.5v497q54-26 154-57 55-17 87.5-29.5t70.5-31 59-39.5 40.5-51 28-69.5 8.5-91.5q-44-25-70-69.5t-26-96.5q0-80 56-136t136-56 136 56 56 136z"',
         'star': 'viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg"><path d="M1201 1004l306-297-422-62-189-382-189 382-422 62 306 297-73 421 378-199 377 199zm527-357q0 22-26 48l-363 354 86 500q1 7 1 20 0 50-41 50-19 0-40-12l-449-236-449 236q-22 12-40 12-21 0-31.5-14.5t-10.5-35.5q0-6 2-20l86-500-364-354q-25-27-25-48 0-37 56-46l502-73 225-455q19-41 49-41t49 41l225 455 502 73q56 9 56 46z"'}

def main():
    config = json.load(open(CONFIG_FILE))
    template = open(SRCFILE).read()
    project_data = projects(config['gh-name'], OTHER_PROJECTS)
    out = jinja2.Template(template).render({"projects": project_data,
                                            "pages": pages(PAGES_DIR),
                                            "icons": ICONS})
    open(DESTFILE, 'w').write(out)

    return 0
