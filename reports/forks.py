"""Self contained util to collect number of forks of a github project."""

import json
import os
from github import Github

from cache import Cache

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(SCRIPT_DIR, './config.json')
CACHE = Cache(os.path.join(SCRIPT_DIR, "./forks_cache.json"))

def get_total_forks(user, project):
    """Get total number of forks of a project."""
    cache_key = f"{user}/{project}"
    if CACHE.has_key(cache_key):
        return CACHE.get_value(cache_key)
    cache_value = get_total_forks_no_cache(user, project)
    CACHE.set_value(cache_key, cache_value)
    return cache_value

def get_total_forks_no_cache(user, project):
    """Get total number of forks of a project without caching results."""
    repo = get_repo(user, project)
    if repo:
        return repo.forks
    return None

_GITHUB_API = None
def _get_github_api():
    """Init Github API client."""
    # authenticate github api
    global _GITHUB_API
    if _GITHUB_API is None:
        _GITHUB_API = Github(
            login_or_token=config_get('github_token')
        )
    return _GITHUB_API

def get_repo(user, project):
    """Get repo of a repository."""
    try:
        return _get_github_api().get_user(user).get_repo(project)
    except:
        print(f"Error: could not find gh project {user}/{project}.")
    return None


def config_get(config_key):
    """Get value of a configuration config_key."""
    with open(CONFIG_PATH) as config_file:
        config = json.load(config_file)
        value = config.get(config_key)
        if not value:
            print("Warning: no config value found for {}.".format(config_key))
        return value
