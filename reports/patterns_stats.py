"""Parse yaml specification of patterns and export to latex."""

import pprint as pp
import yaml
import csv

YAML_FILE = '../docs/patterns.yml'
IOS_CLEAN_SUBJECTS = '../clean_results/energy_mentions_ios.csv'
ANDROID_CLEAN_SUBJECTS = '../clean_results/energy_mentions_android.csv'

def main():
    """Execute main script."""
    pprint = pp.PrettyPrinter(indent=4).pprint

    # Patterns Stats
    print("-------------")
    print("Pattern Stats")
    print("-------------")
    with open(YAML_FILE, 'r') as patterns_yml:
        results = {}
        try:
            patterns = yaml.load(patterns_yml)
            results['android_commits'] = sum(len(pattern.get('occurrences_android', {}).get('commits', [])) for pattern in patterns)
            results['ios_commits'] = sum(len(pattern.get('occurrences_ios', {}).get('commits', [])) for pattern in patterns)
            results['android_issues'] = sum(len(pattern.get('occurrences_android', {}).get('issues', [])) for pattern in patterns)
            results['ios_issues'] = sum(len(pattern.get('occurrences_ios', {}).get('issues', [])) for pattern in patterns)
            results['android_pull_requests'] = sum(len(pattern.get('occurrences_android', {}).get('pull_requests', [])) for pattern in patterns)
            results['ios_pull_requests'] = sum(len(pattern.get('occurrences_ios', {}).get('pull_requests', [])) for pattern in patterns)
            pprint(results)
            
            total = sum(results.values())
            print("Total subjects: {}".format(total))

            total_ios = sum(results[key] for key in ('ios_commits', 'ios_issues', 'ios_pull_requests'))
            print("Total subjects ios: {}".format(total_ios))

            total_android = sum(results[key] for key in ('android_commits', 'android_issues', 'android_pull_requests'))
            print("Total subjects android: {}".format(total_android))
            
            total_commits = results['ios_commits'] + results['android_commits']
            print("Total subjects commits: {}".format(total_commits))
            
            total_issues = results['ios_issues'] + results['android_issues']
            print("Total subjects issues: {}".format(total_issues))
            
            total_pull_requests = results['ios_pull_requests'] + results['android_pull_requests']
            print("Total subjects pull_requests: {}".format(total_pull_requests))
            
        except yaml.YAMLError as exc:
            print(exc)
    
    # Energy Mentions
    print("---------------------")
    print("Energy Mentions Stats")
    print("---------------------")
    results = {}
    TYPE_COL = 5
    URL_COL = 2
    #ios
    with open(IOS_CLEAN_SUBJECTS, 'r') as ios_mentions_csv:
        ios_mentions = list(csv.reader(ios_mentions_csv))[1:]
        results['ios_commits'] = sum(1 for mention in ios_mentions if 'commit' in mention[TYPE_COL])
        results['ios_issues'] = sum(1 for mention in ios_mentions if 'issue' in mention[TYPE_COL] or 'Issue' in mention[TYPE_COL])
        results['ios_pull_requests'] = sum(1 for mention in ios_mentions if 'Pull' in mention[TYPE_COL])
        ios_apps = set([_extract_app(mention[URL_COL]) for mention in ios_mentions])
        results['ios_total_apps'] = len(ios_apps)
        
    #android
    with open(ANDROID_CLEAN_SUBJECTS, 'r') as android_mentions_csv:
        android_mentions = list(csv.reader(android_mentions_csv))[1:]
        for index, mention in enumerate(android_mentions):
            if len(mention) < 6:
                print(index,mention)
        results['android_commits'] = sum(1 for mention in android_mentions if '/commit/' in mention[URL_COL])
        results['android_issues'] = sum(1 for mention in android_mentions if '/issues/' in mention[URL_COL])
        results['android_pull_requests'] = sum(1 for mention in android_mentions if '/pull/' in mention[URL_COL])
        android_apps = set([_extract_app(mention[URL_COL]) for mention in android_mentions])
        results['android_total_apps'] = len(android_apps)
        
        results['total_entries'] = len(android_mentions)+len(ios_mentions)
        results['total_commits'] = results['ios_commits']+results['android_commits']
        results['total_issues'] = results['ios_issues']+results['android_issues']
        results['total_pull_requests'] = results['ios_pull_requests']+results['android_pull_requests']

    pprint(results)

def _extract_app(github_url):
    """Extract app identifier from gihtub url"""
    splits = github_url.split('github.com/')[1].split('/')
    return splits[0]+"/"+splits[1]

if __name__ == '__main__':
    main()
