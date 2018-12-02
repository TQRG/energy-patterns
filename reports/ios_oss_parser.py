import json
import functools

IOS_OSS_APPS_DATASET = "../oss_ios_apps/contents_july_2018.json"

@functools.lru_cache()
def get_project(gh_user, gh_project):
    """Ola."""
    project_name = f"{gh_user}/{gh_project}"
    datastore = _read_app_dataset()
    projects = datastore['projects']
    return next(
        (project
         for project in projects
         if project_name in project['source']),
        None
    )

@functools.lru_cache()
def get_itunes_id(gh_user, gh_project):
    project = get_project(gh_user, gh_project)
    itunes_url = project.get('itunes')
    if itunes_url:
        return itunes_url.split('/id')[-1]
    return None

@functools.lru_cache()
def _read_app_dataset():
    """Parse json object with app informatino."""
    with open(IOS_OSS_APPS_DATASET, 'r') as input_file:
        datastore = json.load(input_file)
    return datastore
