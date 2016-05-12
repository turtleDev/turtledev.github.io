# -*- coding: utf-8 -*-

'''
    TODO: use a markdown library
'''

import os
import codecs

def pages(path):
    rendered = []
    top = os.walk(path).next()
    base = top[0]
    files = top[2]
    files.sort()
    for k in files:
        path = os.path.join(base, k)
        item = {'content': codecs.encode(os.popen('markdown {}'.format(path)).read(), 'UTF-8'),
                'name': k}
        rendered.append(item)
    return rendered
