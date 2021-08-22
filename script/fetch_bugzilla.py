import time
import bugzilla
import json 
from datetime import datetime
import argparse
import os

def fetch(project):
    project = "MAT"
    pathOutput = ""
    URL = "https://bugs.eclipse.org/bugs/rest/"
    bzapi = bugzilla.Bugzilla(URL, force_rest=True)

    query = bzapi.build_query()
    query["product"] = project,
    query["status"] = ["RESOLVED", "VERIFIED", "CLOSED"]
    query["resolution"] = "FIXED"

    bugs = bzapi.query(query)

    reports=[]
    comments=[]
    for bug in bugs :
        print(bug.id)
        commentsRaw=bug.getcomments()
        commentsSeq=""
        for comment in commentsRaw:
            dateCreated = datetime.strptime(str(comment["creation_time"]), "%Y-%m-%dT%H:%M:%SZ")
            c = {
                "bugID":comment["bug_id"] ,
                "developer":comment["creator"],
                "date":str(int(dateCreated.timestamp()))+"000",
                "comment": comment["text"]
            }
            commentsSeq+=c["comment"]
            comments.append(c)
        dateCreatedTmp = datetime.strptime(str(bug.creation_time), "%Y-%m-%dT%H:%M:%SZ")
        dateResolvedTmp = datetime.strptime(str(bug.last_change_time), "%Y-%m-%dT%H:%M:%SZ")
        #dateCreated = dateCreatedTmp.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
        #dateResolved = dateResolvedTmp.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
        dateCreated = str(int(dateCreatedTmp.timestamp())) + "000"
        dateResolved = str(int(dateResolvedTmp.timestamp())) + "000"
        report = {
            "bugId": bug.id,
            "Type": bug.priority,
            "Status": bug.resolution,
            "Owner": bug.assigned_to_detail["real_name"],
            "Reporter": bug.creator_detail["real_name"],
            "ReportDate": dateCreated,
            "ModifiedDate": dateResolved,
            "LastDate": dateResolved,
            "Summary": bug.summary,
            "Comments": commentsSeq
        }
        reports.append(report)

    with open('reports.json', 'w', encoding="utf-8") as f:
        json.dump(reports, f, indent=4)
    with open('comments.json', 'w', encoding="utf-8") as f:
        json.dump(comments, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--project', type=str)

    args = parser.parse_args()
    project = args.project
    fetch(project)