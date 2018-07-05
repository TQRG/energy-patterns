#!/usr/bin/env python

import json
import csv
import re
import time
from random import randrange
from random import randint

from itertools import chain

import requests.exceptions
import click
from github import Github
from github.GithubException import GithubException

REQUEST_WAIT = 60
CSV_OUTPUT = 'energy-matches.csv'
CSV_HEADER = [
    'user',
    'repo',
    'url',
    'ref',
    'match',
    'contribution_type'
]


# authenticate github api
with open('./config.json') as config_file:
    config = json.load(config_file)

# regex to match commit messages
PATTERN_ENERGY = "(.*(energy).*)|(.*(battery).*)|(.*(power).*)"
regexEnergy = re.compile(PATTERN_ENERGY, re.IGNORECASE)

_github_api = None
def get_github_api():
    """Init Github API client."""
    # authenticate github api
    global _github_api
    if _github_api is None:
        with open('./config.json') as config_file:
            config = json.load(config_file)
        _github_api = Github(
            login_or_token=config.get('github_token')
        )
    return _github_api


def get_repo(organization, project):
    """Get commits of a repository."""
    return get_github_api().get_user(organization).get_repo(project)


def analyze_repo(user, project, retry=120):
    """Find pattern a given repository."""
    result = []
    try:
        repo = get_repo(user, project)
        commits = repo.get_commits()
        for commit in commits:
            commit_message = commit.commit.message
            match = regexEnergy.search(commit_message)
            if match:
                print('----------------')
                print("Repo {}/{}".format(user, repo))
                print(commit_message)
                print(commit.html_url)
                result.append({
                    'user': user,
                    'repo': project,
                    'url': commit.html_url,
                    'ref': commit.sha,
                    'match': match.group(0),
                    'contribution_type': 'commit_message'
                })
        pull_requests = repo.get_pulls(state='all')
        issues_all = repo.get_issues(state='all') # somehow also collects PRs
        issues = (issue for issue in issues_all if issue.pull_request is None)
        for subject in chain(issues, pull_requests):
            content = "\n".join([
                subject.title,
                str(subject.body),
            ]+[str(comment.body) for comment in subject.get_comments()])
            match = regexEnergy.search(content)
            if match:
                result.append({
                    'user': user,
                    'repo': project,
                    'url': subject.html_url,
                    'ref': subject.number,
                    'match': match.group(0),
                    'contribution_type': type(subject).__name__
                })

    except requests.exceptions.HTTPError as error:
        print(
            "Error in repo {}/{}: 403 forbidden -- {}"
            "".format(user, repo, error.message)
        )
        if retry:
            print("Will retry in 1 minute.")
            time.sleep(REQUEST_WAIT*randrange(0.7, 1.4, 0.1))
            return analyze_repo(user, repo, retry-1)
    return result


@click.argument('input_path', default="hall_of_fame.csv",
                type=click.Path(dir_okay=False))
@click.argument('output_path', default="results.csv",
                type=click.Path(dir_okay=False))
@click.option('--history', type=click.Path(dir_okay=False))
@click.command()
def main(input_path, output_path, history):
    """Process github repos."""
    history_list = None
    if history:
        with open(history, 'r') as history_file:
            history_list = history_file.read().splitlines()

    with open(input_path, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        for app in csv_reader:
            try:
                app_uri = "{}/{}".format(app['user'], app['project_name'])
                click.secho(
                    'Processing {}'.format(app_uri),
                    fg='blue'
                )
                if history_list and (app_uri in history_list):
                    click.secho(
                        'History: {} already processed'.format(app_uri),
                        fg='green'
                    )
                    continue
                results = analyze_repo(app['user'], app['project_name'])
                with open(output_path, 'a') as output_file:
                    csv_writer = csv.DictWriter(
                        output_file,
                        fieldnames=CSV_HEADER
                    )
                    csv_writer.writerows(results)
                if history:
                    with open(history, 'a') as history_file:
                        history_file.write(app_uri+"\n")

            except GithubException as exception:
                print(exception)
                print(exception.args)
                print("Skipping repo {}/{}: {}.".format(
                    app['user'],
                    app['project_name'],
                    exception.data['message']
                ))
                if exception.status == 403:
                    #sleep 1--2minutes
                    time.sleep(randint(60, 120))
            #pretend this is not a bot
            time.sleep(randint(1, 10))


def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Script exited in {:.2f} minutes.".format(duration/60),
        fg='green'
    )


if __name__ == '__main__':
    START_TIME = time.time()
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully(START_TIME)
