# -*- coding: utf-8 -*-

import sys
import logging

import requests

logger = logging.getLogger(__name__)

def transform(repo):
    return {'name': repo['name'],
            'url': repo['html_url'],
            'description': repo['description'],
            'forks': repo['forks'],
            'watchers': repo['watchers'],
            'stars': repo['stargazers_count']}

def gh_projects(username):
    '''returns a list of github projects of :username:
    along with some metadata
    '''

    repo_url = "https://api.github.com/users/{username}/repos".format(
        username=username)

    try:
        r = requests.get(repo_url)
    except:
        e = sys.exc_info()[1]
        logger.warning('unable to download data from github ({})'.format(e))
        return []


    repos = json.loads(r.content)
    repos = filter(lambda r: r['fork'] is False, repos)
    repos = map(transform, repos)
    return repos
