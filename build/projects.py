# -*- coding: utf-8 -*-

import sys
import logging
import json

import requests

logger = logging.getLogger(__name__)

def transform(repo):
    return {'name': repo['name'],
            'url': repo['homepage'] or repo['html_url'],
            'description': repo['description'],
            'forks': repo['forks'],
            'watchers': repo['watchers'],
            'stars': repo['stargazers_count']}


def projects(username, other_projects_file=None):
    '''returns a list of github projects of :username:
    along with some metadata
    '''

    repo_url = "https://api.github.com/users/{username}/repos".format(
        username=username)

    try:
        r = requests.get(repo_url)
    except:
        r = {'content': '[]'}
        e = sys.exc_info()[1]
        logger.warning('unable to download data from github ({})'.format(e))


    gh_projects = json.loads(r.content)
    gh_projects = filter(lambda r: r['fork'] is False, gh_projects)
    gh_projects = map(transform, gh_projects)

    try:
        other_projects = json.load(open(other_projects_file))
    except:
        other_projects = []
        e = sys.exc_info()[1]
        logger.warning('unable to load data for other projects from file {} [{}]'.format(other_projects_file, e))


    return gh_projects + other_projects
