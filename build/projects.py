# -*- coding: utf-8 -*-

import logging

import requests

logger = logging.getLogger(__name__)

def gh_projects(username):
    '''returns a list of github projects of :username:
    along with some metadata
    '''

    repo_url = "https://api.github.com/users/{username}/repos".format(
        username=username)

    try:
        r = requests.get(repo_url)
        repos = json.loads(r.content)
    except:
        e = sys.exc_info().pop()
        logger.warning('unable to download or parse repo data from github')
        logger.warning(e)
        return []

    def transform(repo):
        return {'name': repo['name'],
                'url': repo['html_url'],
                'description': repo['description'],
                'forks': repo['forks'],
                'watchers': repo['watchers'],
                'stars': repo['stargazers_count']}

    repos = filter(lambda r: r['fork'] is False, repos)
    repos = map(transform, repos)
    return repos
