# 取得するやつ
# key: Jenkins-27380とか
# creationdate
# resolutiondate

import requests, os
import json
import argparse

def fetch(owner, project, pathOutput):
    d={}
    d["total"]=0
    d["issues"]=[]

    page=1
    while(True):
        url = 'https://api.github.com/repos/' + owner + '/' + project + '/issues?state=closed&labels=bug&per_page=100&page='+str(page)
        print(url)
        res = requests.get(url)
        issues = json.loads(res.text)
        if(len(issues)==0):
            break
        d["issues"].extend(issues)
        page=page+1
    d["total"]=len(d["issues"])

    with open('reports.json', 'w', encoding="utf-8") as f:
        json.dump(d, f, indent=4)


#while start_at < total:
#    with url.urlopen(request.format(jql, start_at, max_results)) as conn:
#        dTmp = json.loads(conn.read().decode('utf-8'))
#        for issue in dTmp["issues"]:
#            id =issue["key"]
#            dateCreated = str(issue["fields"]["created"])
#            dateResolved = str(issue["fields"]["resolutiondate"])
#            fields = {"created":dateCreated, "resolutiondate":dateResolved}
#            row={"key":id ,"fields":fields}
#            d["issues"].append(row)
#    print('|', end='', flush='True')
#    start_at += max_results
#if(0<len(pathOutput)):
#    os.makedirs(pathOutput, exist_ok=True)
#    with open(os.path.join(pathOutput, 'reports.json'), 'w', encoding="utf-8") as f:
#        json.dump(d, f, indent=4)
#else:
#    with open('reports.json', 'w', encoding="utf-8") as f:
#        json.dump(d, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--owner', type=str)
    parser.add_argument('--project', type=str)
    parser.add_argument('--pathOutput', type=str, default="", help="dest")

    args = parser.parse_args()
    owner = args.owner
    project = args.project
    pathOutput        = args.pathOutput
    fetch(owner, project, pathOutput)
