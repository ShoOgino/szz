""" Fetch issues that match given jql query """
__author__ = "Kristian Berg"
__copyright__ = "Copyright (c) 2018 Axis Communications AB"
__license__ = "MIT"

from urllib.parse import quote

import urllib.request as url
import json
import os
import argparse
import io
import sys

def fetch(project_issue_code, jira_project_name, pathOutput):
    """ Fetch issues that match given jql query """
    # Jira Query Language string which filters for resolved issues of type bug
    jql = 'project = ' + project_issue_code + ' ' \
        + 'AND issuetype = Bug '\
        + 'AND status in (Resolved, Closed) '\
        + 'AND resolution = Fixed'
    jql = quote(jql, safe='')

    start_at = 0

    # max_results parameter is capped at 1000, specifying a higher value will
    # still return only the first 1000 results
    max_results = 1000

    request = 'https://' + jira_project_name + '/rest/api/2/search?'\
        + 'jql={}&startAt={}&maxResults={}'

    # Do small request to establish value of 'total'

    with url.urlopen(request.format(jql, start_at, '1')) as conn:
        contents = json.loads(conn.read().decode('utf-8'))
        total = contents['total']

    # Fetch all matching issues and write to file(s)
    print(request.format(jql, start_at, max_results))
    print('Total issue matches: ' + str(total))
    d={}
    d["total"]=total
    d["issues"]=[]
    while start_at < total:
        with url.urlopen(request.format(jql, start_at, max_results)) as conn:
            dTmp = json.loads(conn.read().decode('utf-8'))
            for issue in dTmp["issues"]:
                id =issue["key"]
                dateCreated = str(issue["fields"]["created"])
                dateResolved = str(issue["fields"]["resolutiondate"])
                fields = {"created":dateCreated, "resolutiondate":dateResolved}
                row={"key":id ,"fields":fields}
                d["issues"].append(row)
        print('|', end='', flush='True')
        start_at += max_results
    if(0<len(pathOutput)):
        os.makedirs(pathOutput, exist_ok=True)
        with open(os.path.join(pathOutput, 'reports.json'), 'w', encoding="utf-8") as f:
            json.dump(d, f, indent=4)
    else:
        with open('reports.json', 'w', encoding="utf-8") as f:
            json.dump(d, f, indent=4)

    print('\nDone!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--issue-code', type=str, help="The code used for the project issues on JIRA: e.g., JENKINS-1123. Only JENKINS needs to be passed as parameter.")
    parser.add_argument('--jira-project', type=str, help="The name of the Jira repository of the project.")
    parser.add_argument('--pathOutput', type=str, default="", help="dest")

    args = parser.parse_args()
    project_issue_code = args.issue_code
    jira_project_name  = args.jira_project
    pathOutput        = args.pathOutput
    fetch(project_issue_code, jira_project_name, pathOutput)