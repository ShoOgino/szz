import argparse
import subprocess
import sys
import json
from pydriller import Repository, ModificationType
import csv

def git_log_to_json(pathRepository, commitFrom):
    pathRepository = r"C:\Users\login\work\buggyChangeLocater\projects\egit\repositoryMethod"
    commitFrom = "b459d7381ea57e435bd9b71eb37a4cb4160e252b"
    commits = []
    for i, commit in enumerate(Repository(pathRepository, to_commit=commitFrom).traverse_commits()):
        comment = commit.msg.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("	", " ")
        comment = comment + " Modified : None"
        for modified_file in commit.modified_files:
            if(modified_file.change_type==ModificationType.ADD):
                comment = comment + " Added : " + modified_file.new_path
            elif(modified_file.change_type==ModificationType.DELETE):
                comment = comment + " Deleted : " + modified_file.old_path
            else:
                comment = comment + " Modified : " + modified_file.new_path
        row={}
        row["id"]=i#commit.hash
        row["author"]=commit.author.name
        row["date"]=str(int(commit.committer_date.timestamp()))+"000"#.strftime("%Y-%m-%d %H:%M:%S %z")#2020-07-24     23:52:45 +0200
        row["comment"] = comment
        commits.append(row)
    with open('commits.csv', 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        count =0
        for commit in commits:
            count+=1
            writer.writerow(
                [
                    commit["id"],
                    commit["date"],
                    commit["author"],
                    commit["comment"]
                ]
            )


# Commits are saved in reverse chronological order from newest to oldest
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""Convert a git log output to json.
                                                 """)
    parser.add_argument('--pathRepository', type=str)
    parser.add_argument('--commitFrom', type=str)

    args = parser.parse_args()
    pathRepository = args.pathRepository
    commitFrom = args.commitFrom
    git_log_to_json(pathRepository, commitFrom)