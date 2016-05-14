# -*- coding: utf-8 -*-

'''
    TODO: use a markdown library
'''

import os
import codecs


from markdown import markdown

def pages(path):
    rendered = []
    top = os.walk(path).next()
    base = top[0]
    files = top[2]
    files.sort()
    for k in files:
        path = os.path.join(base, k)
        item = {'content': markdown(codecs.open(path, 'r', 'UTF-8').read()),
                'name': k}
        rendered.append(item)
    return rendered
