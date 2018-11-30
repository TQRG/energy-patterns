"""Self contained util to collect number of forks of a github project."""

import json
import os
from github import Github

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(SCRIPT_DIR, './config.json')

def get_total_forks(user, project):
    """Get total number of forks of a project."""
    cache_key = f"{user}/{project}"
    cache_value = CACHE.get_value(cache_key)
    if cache_value:
        return cache_value
    cache_value = get_total_forks_no_cache(user, project)
    CACHE.set_value(cache_key, cache_value)
    return cache_value

def get_total_forks_no_cache(user, project):
    """Get total number of forks of a project without caching results."""
    repo = get_repo(user, project)
    return len(list(repo.forks))

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


class Cache():
    """Cache in json."""
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self._data = None

    @property
    def data(self):
        """Return dict with all cached data."""
        if self._data is None:
            try:
                with open(self.storage_path, 'r') as cache_file:
                    self._data = json.load(cache_file)
            except FileNotFoundError:
                self._data = {}
        return self._data

    def get_value(self, key):
        """Return value for given key."""
        return self.data.get(key)

    def set_value(self, key, value):
        """Set value for given key."""
        self.data[key] = value
        self.save_data()

    def remove_key(self, key):
        """Remove a key from cache."""
        del self.data[key]
        self.save_data()

    def save_data(self):
        """Store data in designated json file."""
        with open(self.storage_path, 'w') as cache_file:
            json.dump(self.data, cache_file)

CACHE = Cache(os.path.join(SCRIPT_DIR, "./forks_cache.json"))
