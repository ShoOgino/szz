""" Dump the git log to a file """
__author__ = "Kristian Berg"
__copyright__ = "Copyright (c) 2018 Axis Communications AB"
__license__ = "MIT"
__credits__ = ["Kristian Berg", "Oscar Svensson"]

import argparse
import subprocess
import sys
import json
from pydriller import GitRepository, RepositoryMining, domain

def git_log_to_json(commitFrom, pathRepository):
    d=[]
    for commit in RepositoryMining(pathRepository, to_commit=commitFrom).traverse_commits():
        row={}
        row["id"]=commit.hash
        row["date"]=commit.committer_date.strftime("%Y-%m-%d %H:%M:%S %z")#2020-07-24 23:52:45 +0200
        row["comment"]=commit.msg
        d.insert(0, row)
    with open('commits.json', 'w') as f:
        json.dump(d, f)


# Commits are saved in reverse chronological order from newest to oldest
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""Convert a git log output to json.
                                                 """)
    parser.add_argument('--commitFrom', type=str,
            help="A SHA-1 representing a commit. Runs git rev-list from this commit.")
    parser.add_argument('--pathRepository', type=str,
            help="The absolute path to a local copy of the git repository from where the git log is taken.")

    args = parser.parse_args()
    pathRepository = args.pathRepository
    commitFrom = args.commitFrom
    git_log_to_json(commitFrom, pathRepository)

