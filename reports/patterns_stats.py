"""Parse yaml specification of patterns and export to latex."""

import pprint as pp
import yaml

YAML_FILE = '../docs/patterns.yml'

def main():
    """Execute main script."""
    pprint = pp.PrettyPrinter(indent=4).pprint

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

        except yaml.YAMLError as exc:
            print(exc)

if __name__ == '__main__':
    main()
