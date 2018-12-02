import os

import requests

import cache

SCRIPT_DIR = os.path.dirname(__file__)
CACHE = cache.Cache(os.path.join(SCRIPT_DIR, "./itunes_cache.json"))

@cache.persistent_cache(CACHE, save_nulls=True)
def _get_itunes_data(app_id):
    url = f'http://itunes.apple.com/lookup?id={app_id}'
    response = requests.get(url=url)
    results = response.json().get('results')
    if results:
        return results[0]
    return None

def get_reviews_count(app_id):
    """Get number of ratings for app id."""
    app_data = _get_itunes_data(app_id)
    if app_data:
        return app_data.get('userRatingCount')
    return None

def get_reviews_avg(app_id):
    """Get number of ratings for app id."""
    app_data = _get_itunes_data(app_id)
    if app_data:
        return app_data.get('averageUserRating')
    return None

def _get_itunes_data_old(app_id, page):
    url = f'https://itunes.apple.com/rss/customerreviews/id={app_id}/page={page}/sortby=mostrecent/json'
    response = requests.get(url=url)
    return response.json()

def get_reviews_count_old(app_id):
    """Get number of ratings for app id."""
    try:
        app_data_first_page = _get_itunes_data(app_id, 1)
        reviews_count_first_page = _feed_get_reviews_count(app_data_first_page)
        last_page_number = _feed_get_last_page_number(app_data_first_page)
        if last_page_number > 1:
            app_data_last_page = _get_itunes_data(app_id, last_page_number)
            reviews_count_last_page = _feed_get_reviews_count(app_data_last_page)
            reviews_count =  reviews_count_first_page*(last_page_number-1) + reviews_count_last_page
            return reviews_count
        else:
            return reviews_count_first_page
    except NoAppEntry:
        return None

def _feed_get_reviews_count(app_data):
    return len(_feed_get_reviews(app_data))

def _feed_get_reviews(app_data):
    return app_data.get("feed", {}).get('entry', [])

def _feed_get_last_page_number(app_data):
    links = app_data['feed']['link']
    link_href = next(
        link['attributes']['href']
        for link in links
        if link['attributes']['rel'] == 'last'
    )
    if link_href:
        page = link_href.split('customerreviews/page=')[1].split('/')[0]
        return int(page)
    raise NoAppEntry


class NoAppEntry(Exception):
    """Exception raise when the app is not listed in iTunes."""
    pass