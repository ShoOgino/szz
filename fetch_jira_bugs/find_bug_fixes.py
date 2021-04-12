import os
import json
import re
import argparse
from tqdm import tqdm

def find_bug_fixes(pathReport, pathCommits):
    with open(pathReport, encoding="utf-8") as f:
        reports = json.loads(f.read())["issues"]
    bugfixes = {}
    issuesUnmatched = []
    commits = []
    with open(pathCommits, encoding="utf_8") as f:
        commits = json.loads(f.read())

    for report in tqdm(reports):
        count = 0
        commitsMatched = []
        key = report["key"]
        pattern = r'^{key}$|^{key}\W|\W{key}\W|\W{key}$'.format(key=key)
        for commit in commits:
            if re.search(pattern, commit["comment"]):
                #print("   match: " + pattern + " " + str(count))
                bugfixes[key+"_"+str(count)]={}
                bugfixes[key+"_"+str(count)]['hash'] = commit["id"]
                bugfixes[key+"_"+str(count)]['commitdate'] = commit["date"]
                created_date = report['fields']['created'].replace('T', ' ')
                created_date = created_date.replace('.000', ' ')
                bugfixes[key+"_"+str(count)]['creationdate'] = created_date
                res_date = report['fields']['resolutiondate'].replace('T', ' ')
                res_date = res_date.replace('.000', ' ')
                bugfixes[key+"_"+str(count)]['resolutiondate'] = res_date
                count+=1
        if count == 0:
            #print("no match: " + pattern)
            issuesUnmatched.append(key)

    print('Total issues: ' + str(len(reports)))
    print('Issues matched to a bugfix: ' + str(len(reports) - len(issuesUnmatched)))
    print('Percent of issues matched to a bugfix: ' + \
          str((len(reports) - len(issuesUnmatched)) / len(reports)))

    return bugfixes

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
