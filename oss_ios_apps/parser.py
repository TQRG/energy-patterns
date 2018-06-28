import json
from urllib.parse import urlparse
import time

import click

SKIP_CATEGORIES = frozenset({
    # 'apple-tv',
    # 'apple-watch',
})

def parse_gh_link(url):
    parse = urlparse(url)
    path_items = parse.path.strip().split('/')
    if len(path_items) == 3 and 'github.com' == parse.netloc:
        username = path_items[1]
        repo = path_items[2]
        return username,repo
    return None,None


@click.argument('input_path', default="oss_ios_apps/contents.json",
                type=click.Path(dir_okay=False))
@click.argument('output_path', default="oss_ios_apps/ios_apps.csv",
                type=click.Path(dir_okay=False))
@click.command()
def main(input_path, output_path):
    with open(input_path, 'r') as input_file:
        datastore = json.load(input_file)
    with open(output_path, 'w') as output_file:
        output_file.write(
            "title,"
            "user,"
            "project_name,"
            "stars\n"
        )
        for project in datastore['projects']:
            if not SKIP_CATEGORIES.intersection(project.get('category-ids')):
                username,repo = parse_gh_link(project.get('source'))
                if username:
                    output_file.write(','.join([
                        str(project.get('title')).replace(',', ''),
                        username,
                        repo,
                        str(project.get('stars')),
                    ])+"\n")
            

def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Script executed in {:.2f} minutes.".format(duration/60),
        fg='green'
    )


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully(start_time)
