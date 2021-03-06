"""Parse yaml specification of patterns and export to latex."""

import pprint as pp
import csv
import yaml
import statistics

import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tabulate import tabulate
import tabulate as T
from android_category.android_category import get_app_category_from_repo_git, APP_CATEGORY_CACHE
import pandas as pd

import ios_category
from ios_oss_parser import get_itunes_id
import itunes_app_store as itunes
from forks import get_total_forks

YAML_FILE = '../docs/patterns.yml'
IOS_CLEAN_SUBJECTS = '../clean_results/energy_mentions_ios.csv'
ANDROID_CLEAN_SUBJECTS = '../clean_results/energy_mentions_android.csv'
APPS_DATASET_FROID = '../fdroid_repos.csv'
APPS_DATASET_EXTRA_ANDROID = '../extra_android_oss_repos.csv'
APPS_DATASET_IOS = '../oss_ios_apps/ios_apps_july_2018.csv'

TOTAL_ANDROID_APPS = 1027
TOTAL_IOS_APPS = 756

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
            
            patterns_map = {
                'Avoid Extraneous Graphics and Animations': 'Avoid Extra. Graph. & Anim.'
            }
            patterns_labels = [
                patterns_map.get(pattern.get('name'),pattern.get('name'))
                for pattern in patterns
            ]
            patterns_occurrences_ios = [
                occurrence
                for pattern in patterns
                for occurrence in
                pattern.get('occurrences_ios',{}).get('commits',[])+
                pattern.get('occurrences_ios',{}).get('pull_requests',[])+
                pattern.get('occurrences_ios',{}).get('issues',[])
            ]
            patterns_apps_ios_count = len(set(_extract_app(occurrence) for occurrence in patterns_occurrences_ios))
            print("Number of iOS apps with patterns: {}".format(patterns_apps_ios_count))
            patterns_count_ios = np.array([
                len(pattern.get('occurrences_ios',{}).get('commits',[]))+
                len(pattern.get('occurrences_ios',{}).get('pull_requests',[]))+
                len(pattern.get('occurrences_ios',{}).get('issues',[]))
                for pattern in patterns
            ])
            patterns_count_android = np.array([
                len(pattern.get('occurrences_android',{}).get('commits',[]))+
                len(pattern.get('occurrences_android',{}).get('pull_requests',[]))+
                len(pattern.get('occurrences_android',{}).get('issues',[]))
                for pattern in patterns
            ])

            patterns_occurrences_android = [
                occurrence
                for pattern in patterns
                for occurrence in
                pattern.get('occurrences_android',{}).get('commits',[])+
                pattern.get('occurrences_android',{}).get('pull_requests',[])+
                pattern.get('occurrences_android',{}).get('issues',[])
                for pattern in patterns
            ]
            apps_android = list(set(_extract_app(occurrence) for occurrence in patterns_occurrences_android))
            patterns_apps_android_count = len(apps_android)
            print("Number of Android apps with patterns: {}".format(patterns_apps_android_count))
            fig, ax = plt.subplots()
            width = 0.35
            index = np.arange(len(patterns_labels))
            rects1 = ax.bar(index-width/2, patterns_count_android/TOTAL_ANDROID_APPS, width, color='C2', alpha=0.7)
            rects2 = ax.bar(index + width/2, patterns_count_ios/TOTAL_IOS_APPS, width, color='red', alpha=0.7)
            ax.set_xticklabels(patterns_labels, rotation='vertical')
            ax.set_xticks(range(len(patterns_labels)))
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.yaxis.grid(linestyle='dotted')
            
            ax.set_ylabel("$R$")
            ax.set_xlabel("Energy Pattern")
            ax.legend((rects1[0], rects2[0]), ('Android', 'iOS'))
            
            fig.tight_layout()
            fig.savefig('reports/pattern_prevalence.pdf')
            report_stars()
            app_categories(apps_android, [])
            chord_diagram(patterns)
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

def _extract_repo_url(github_url):
    return f"https://www.github.com/{_extract_app(github_url)}.git"

def _remove_nulls(collection):
    return [item for item in collection if item is not None]

def report_stars():
    with open(APPS_DATASET_FROID, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        fdroid_apps = list(csv_reader)
    with open(APPS_DATASET_FROID, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        extra_android_apps = list(csv_reader)
    with open(APPS_DATASET_IOS, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        ios_apps = list(csv_reader)
    stars_android = [int(app['stars']) for app in fdroid_apps + extra_android_apps]
    stars_ios = [int(app['stars']) for app in ios_apps if app['stars'] != 'None']
    forks_android = _remove_nulls([get_total_forks(app['user'], app['project_name']) for app in fdroid_apps + extra_android_apps])
    forks_ios = _remove_nulls([get_total_forks(app['user'], app['project_name']) for app in ios_apps])
    # forks_android = _remove_nulls([get_total_forks(app['user'], app['project_name']) for app in fdroid_apps + extra_android_apps])
    ios_itunes_ids = _remove_nulls([get_itunes_id(app['user'], app['project_name']) for app in ios_apps])
    reviews_counts_android = [int(float(app['rating_count'])) for app in fdroid_apps + extra_android_apps if app['rating_count']]
    reviews_counts_ios = _remove_nulls([itunes.get_reviews_count(itunes_id) for itunes_id in ios_itunes_ids])    
    reviews_values_android = [int(float(app['rating_value'])) for app in fdroid_apps + extra_android_apps if app['rating_value']]
    reviews_values_ios = _remove_nulls([itunes.get_reviews_avg(itunes_id) for itunes_id in ios_itunes_ids])    
    print(f"From {len(fdroid_apps + extra_android_apps)} android apps, {len(reviews_values_android)} are available on Google Play Store.")
    print(f"From {len(ios_apps)} ios apps, {len(reviews_values_ios)} are available on iOS App Store.")
    stats = [
        {"Platform": "Android", **_get_stats(stars_android)},
        {"Platform": "iOS", **_get_stats(stars_ios)},
        {"Platform": "Android", **_get_stats(forks_android)},
        {"Platform": "iOS", **_get_stats(forks_ios)},
        {"Platform": "Android", **_get_stats(reviews_counts_android)},
        {"Platform": "iOS", **_get_stats(reviews_counts_ios)},
        {"Platform": "Android", **_get_stats(reviews_values_android)},
        {"Platform": "iOS", **_get_stats(reviews_values_ios)},
    ]
    old_escape_rules = T.LATEX_ESCAPE_RULES
    T.LATEX_ESCAPE_RULES = {'%': '\\%'}
    table = tabulate(
        stats,
        headers='keys',
        showindex=['Stars', 'Stars', 'Forks', 'Forks', 'Number of Reviews', 'Number of Reviews', 'Rating', 'Rating'],
        tablefmt='latex',
        floatfmt=".1f",
    )
    T.LATEX_ESCAPE_RULES = old_escape_rules
    with open("reports/app_stars.tex", 'w') as f:
        f.write(table)
 
def _get_stats(sample):
    return {
        'Mean': statistics.mean(sample),
        'Std': statistics.pstdev(sample),
        'Min': min(sample),
        '25%': np.percentile(sample, 25),
        'Median': statistics.median_high(sample),
        '75%': np.percentile(sample, 75),
        'Max': max(sample),
    }

def app_categories(apps_android, apps_ios):
    """Reports for apps categories"""
    # android_categories = []
    # for app in apps_android:
    #     try:
    #         android_categories.append(
    #             get_app_category_from_repo_git(f"https://www.github.com/{app}.git")
    #         )
    #     except:
    #         continue
    # print(android_categories)
    android_categories_map = {
        'PRODUCTIVITY' : 'Time',
        'MUSIC_AND_AUDIO' : 'Multimedia',
        'GAME_CASUAL' : 'Games',
        'COMMUNICATION' : 'Phone & SMS',
        'ENTERTAINMENT' : 'Multimedia',
        'BOOKS_AND_REFERENCE' : 'Reading',
        'TOOLS' : 'System',
        'BUSINESS' : 'Money',
        'LIFESTYLE' : 'Sports & Health',
    }
    
    with open(APPS_DATASET_FROID, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        fdroid_apps = list(csv_reader)
    categories_fdroid = [android_categories_map.get(app['category'], app['category']) for app in fdroid_apps]
    with open(APPS_DATASET_EXTRA_ANDROID, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        extra_android_apps = list(csv_reader)
    categories_extra_android = []
    
    for app in extra_android_apps:
        app_repo_url = f"https://www.github.com/{app['user']}/{app['project_name']}.git"
        try:
            # category = get_app_category_from_repo_git(app_repo_url)
            category = APP_CATEGORY_CACHE.get_value(app_repo_url)
            category = android_categories_map.get(category, category)
        except:
            print(app_repo_url)
            category = None
            APP_CATEGORY_CACHE.set_value(app_repo_url, category)
        categories_extra_android.append(category)
    android_categories = categories_fdroid + categories_extra_android
    with open(APPS_DATASET_IOS, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        ios_apps = list(csv_reader)
    ios_categories = [ios_category.get_category(app['user'], app['project_name']) for app in ios_apps]
    
    figure, ax = plt.subplots(figsize=(5, 4))
    sns.countplot(android_categories, color='darkgreen', alpha=0.7, ax=ax)
    ax.xaxis.set_tick_params(rotation=90)
    ax.set_ylabel('Count')
    ax.yaxis.grid(linestyle='dotted', color='gray')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    figure.tight_layout()
    figure_path = 'reports/android_app_categories.pdf'
    figure.savefig(figure_path)
    figure, ax = plt.subplots(figsize=(5, 4))
    sns.countplot(ios_categories, color='red', alpha=0.7, ax=ax)
    ax.xaxis.set_tick_params(rotation=90)
    ax.set_ylabel('Count')
    ax.yaxis.grid(linestyle='dotted', color='gray')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    figure.tight_layout()
    figure_path = 'reports/ios_app_categories.pdf'
    figure.savefig(figure_path)

def _get_all_pattern_occurrences(pattern):
    return (
        pattern.get('occurrences_ios', {}).get('commits', [])+
        pattern.get('occurrences_ios', {}).get('pull_requests', [])+
        pattern.get('occurrences_ios', {}).get('issues', [])+
        pattern.get('occurrences_android', {}).get('commits', [])+
        pattern.get('occurrences_android', {}).get('pull_requests', [])+
        pattern.get('occurrences_android', {}).get('issues', [])
    )

def _get_name(pattern):
    patterns_map = {
        'Avoid Extraneous Graphics and Animations': 'Avoid Extra. Graph. & Anim.'
    }
    return patterns_map.get(pattern.get('name'), pattern.get('name'))

def chord_diagram(patterns):
    apps_data = {}
    for pattern in patterns:
        for occurrence in _get_all_pattern_occurrences(pattern):
            app = _extract_app(occurrence)
            previous_patterns = apps_data.get(app, set())
            if previous_patterns is None:
                import pdb; pdb.set_trace()
            previous_patterns.add(_get_name(pattern))
            apps_data[app] = previous_patterns
    pattern_names = [_get_name(pattern) for pattern in patterns]
    chord_data = []
    chord_data_2 = []
    for i1, p1 in enumerate(pattern_names):
        for i2, p2 in enumerate(pattern_names):
            occurrences = len([1 for app_patterns in apps_data.values() if {p1, p2}.issubset(app_patterns)])
            chord_data.append(occurrences)
            chord_data_2.append((p1, p2, occurrences))
    chord_data = np.array(chord_data).reshape(len(pattern_names),len(pattern_names))

    np.savetxt("chord_data.csv", chord_data, delimiter=",")
    pd.DataFrame(chord_data_2).to_csv('chord_data_2.csv', header=False, index=False)

if __name__ == '__main__':
    main()
