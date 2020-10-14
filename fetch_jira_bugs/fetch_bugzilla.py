import time
import bugzilla
import json 
from datetime import datetime
import argparse
import os



def fetch(project, pathOutput):
    URL = "https://bugs.eclipse.org/bugs/xmlrpc.cgi"
    bzapi = bugzilla.Bugzilla(URL)

    query = bzapi.build_query()
    query["product"] = project,
    query["status"] = ["RESOLVED", "VERIFIED", "CLOSED"]
    query["resolution"] = "FIXED"

    bugs = bzapi.query(query)

    d={}
    d["total"]=len(bugs)
    d["issues"]=[]
    for bug in bugs :
        id =str(bug.id)
        dateCreatedTmp = datetime.strptime(str(bug.creation_time), "%Y%m%dT%H:%M:%S")
        dateResolvedTmp = datetime.strptime(str(bug.last_change_time), "%Y%m%dT%H:%M:%S")
        dateCreated = dateCreatedTmp.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
        dateResolved = dateResolvedTmp.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
        fields = {"created":dateCreated, "resolutiondate":dateResolved}
        row={"key":id ,"fields":fields}
        d["issues"].append(row)

    if(0<len(pathOutput)):
        os.makedirs(pathOutput, exist_ok=True)
        with open(os.path.join(pathOutput, 'reports.json'), 'w', encoding="utf-8") as f:
            json.dump(d, f, indent=4)
    else:
        with open('reports.json', 'w', encoding="utf-8") as f:
            json.dump(d, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--project', type=str)
    parser.add_argument('--pathOutput', type=str, default="", help="dest")

    args = parser.parse_args()
    project = args.project
    pathOutput        = args.pathOutput
    fetch(project, pathOutput)