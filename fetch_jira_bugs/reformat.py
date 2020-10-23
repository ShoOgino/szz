import json
import argparse
import os

def reformat(pathInput, pathOutput):
    print(pathInput)
    print(pathOutput)
    historyBugFile={}
    with open(pathInput) as f:
        df = json.load(f)
        for commitFix in df:
            for item in df[commitFix]:
                if(1<len(item["revisions"])):
                    if(not item["filePath"] in historyBugFile):
                        historyBugFile[item["filePath"]]={}
                    if(not commitFix in historyBugFile[item["filePath"]]):
                        historyBugFile[item["filePath"]][commitFix]=[]
                    revisions=[i for i in item["revisions"] if i!=commitFix]
                    historyBugFile[item["filePath"]][commitFix].extend(revisions)
                    #if(commitFix != item["revisions"][0]):
                    #    print(item["filePath"])
                    #    print(commitFix)
        with open(pathOutput, 'w', encoding="utf-8") as f:
            json.dump(historyBugFile, f, indent=4)


def getPathInput(path):
    pathInput=""
    if(0<len(path)):
        pathInput=path
    else:
        pathInput="results/annotations.json"
    return pathInput

def getPathOutput(path):
    pathOutput=""
    if(0<len(path)):
        pathOutput=path
    else:
        pathOutput="bugintros.json"
    return pathOutput


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--pathInput', type=str, default="")
    parser.add_argument('--pathOutput', type=str, default="", help="dest")

    args = parser.parse_args()
    pathInput = getPathInput(args.pathInput)
    pathOutput = getPathOutput(args.pathOutput)

    reformat(pathInput, pathOutput)