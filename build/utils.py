# -*- coding: utf-8 -*-

'''
    utilities
'''

import copy

def merge_dict(base, addon):
    base = copy.deepcopy(base)
    for k,v in addon.items():
        base[k] = v
    return base
