import json
import functools

IOS_OSS_APPS_DATASET = "../oss_ios_apps/contents_july_2018.json"

@functools.lru_cache()
def get_category(gh_user, gh_project):
    """Ola."""
    project_name = f"{gh_user}/{gh_project}"
    datastore = _read_app_dataset()
    projects = datastore['projects']
    return next(
        (_get_category_from_project(project)
         for project in projects
         if project_name in project['source']),
        None
    )

def _get_category_from_project(project):
    useless_categories = [
        'reactive-programming',
        'clone',
        'sample',
        'reactivecocoa',
        'rxswift',
        'bonus'
    ]
    category_map = {
        "color": 'media',
        "scan": 'productivity',
        "timer": 'productivity',
        "clock": 'productivity',
        "calculator": 'productivity',
        "calendar": 'productivity',
        "files": 'productivity',
        "tasks": 'productivity',
        "text": 'productivity',
        "notes": 'productivity',
        "travel": 'location',
        "event": 'social',
    }
    categories = [
        cat_id
        for cat_id in project['category-ids']
        if cat_id not in useless_categories
    ]
    if not categories:
        categories = ['misc']
    category_id = categories[0]
    category_id = category_map.get(category_id, category_id)
    return _get_parent_category_name(category_id)

def _get_parent_category_name(category_id):
    datastore = _read_app_dataset()
    return next(
        ( cat.get('parent') and _get_parent_category_name(cat['parent']) or cat['title']
         for cat in datastore['categories']
         if category_id == cat['id']),
        category_id
    )
    return 

@functools.lru_cache()
def _read_app_dataset():
    """Parse json object with app informatino."""
    with open(IOS_OSS_APPS_DATASET, 'r') as input_file:
        datastore = json.load(input_file)
    return datastore
