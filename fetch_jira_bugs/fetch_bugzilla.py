# 取得するやつ
# key: Jenkins-27380とか
# created
# resolutiondate

import time
import bugzilla
import json 
from datetime import datetime

URL = "https://bugs.eclipse.org/bugs/xmlrpc.cgi"
bzapi = bugzilla.Bugzilla(URL)

if __name__ == '__main__':
    project="EGit"
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
    print(d)
    with open('reports.json', 'w') as f:
        json.dump(d, f)