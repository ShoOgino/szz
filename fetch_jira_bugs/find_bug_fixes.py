import os
import json
import re
import argparse

def find_bug_fixes(issue_path, gitlog_path):
    issues = build_issue_list(issue_path)
    issuesUnmatched = []
    commits = []
    with open(gitlog_path, encoding="utf_8") as f:
        commits = json.loads(f.read())

    for key in issues:
        commitsMatched = []
        pattern = r'{key}\D|{key}$'.format(key=key)
        for commit in commits:
            if re.search(pattern, commit["comment"]):
                commitsMatched.append(commit)
        if commitsMatched:
            selected_commit = commit_selector_heuristic(commitsMatched)
            if not selected_commit:
                issuesUnmatched.append(key)
            else:
                print("match: " + pattern)
                issues[key]['hash'] = selected_commit["id"]
                issues[key]['commitdate'] = selected_commit["date"]
        else:
            print("no match: " + pattern)
            issuesUnmatched.append(key)

    print('Total issues: ' + str(len(issues)))
    print('Issues matched to a bugfix: ' + str(len(issues) - len(issuesUnmatched)))
    print('Percent of issues matched to a bugfix: ' + \
          str((len(issues) - len(issuesUnmatched)) / len(issues)))
    for key in issuesUnmatched:
        issues.pop(key)

    return issues


def build_issue_list(path):
    issues = {}
    with open(path, encoding="utf-8") as f:
        for issue in json.loads(f.read())['issues']:
            issues[issue['key']] = {}

            created_date = issue['fields']['created'].replace('T', ' ')
            created_date = created_date.replace('.000', ' ')
            issues[issue['key']]['creationdate'] = created_date

            res_date = issue['fields']['resolutiondate'].replace('T', ' ')
            res_date = res_date.replace('.000', ' ')
            issues[issue['key']]['resolutiondate'] = res_date
    return issues

def commit_selector_heuristic(commits):
    """ Helper method for find_bug_fixes.
    Commits are assumed to be ordered in reverse chronological order.
    Given said order, pick first commit that does not match the pattern.
    If all commits match, return newest one. """
    for commit in commits:
        if not re.search('[Mm]erge|[Cc]herry|[Nn]oting', commit["comment"]):
            return commit
    return commits[0]

def main():
    """ Main method """
    parser = argparse.ArgumentParser()
    parser.add_argument('--pathReports', type=str, help='Path to directory containing issue json files')
    parser.add_argument('--pathCommits', type=str, help='Path to json file containing gitlog')
    args = parser.parse_args()

    issue_list = find_bug_fixes(args.pathReports, args.pathCommits)
    with open('bugfixes.json', 'w') as f:
        f.write(json.dumps(issue_list))

if __name__ == '__main__':
    main()
