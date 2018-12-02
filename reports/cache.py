"""Module with a class utility for cache in JSON."""

import json
import functools

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

    def has_key(self, key):
        "Check if key has been set."
        return key in self.data.keys()

    def remove_key(self, key):
        """Remove a key from cache."""
        del self.data[key]
        self.save_data()

    def save_data(self):
        """Store data in designated json file."""
        with open(self.storage_path, 'w') as cache_file:
            json.dump(self.data, cache_file)

def persistent_cache(cache_storage, save_nulls=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = "/".join(str(arg) for arg in args)
            if cache_storage.has_key(cache_key):
                return cache_storage.get_value(cache_key)
            return_value = func(*args, **kwargs)
            if save_nulls or return_value is not None:
                cache_storage.set_value(cache_key, return_value)
            return return_value
        return wrapper
    return decorator
    
