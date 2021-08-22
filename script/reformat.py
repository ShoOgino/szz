import json
import argparse
import os

def reformat(pathAnnotation, pathBugFixes, pathOutput):
    print(pathAnnotation)
    print(pathBugFixes)
    print(pathOutput)
    historyBugFile={}
    idBugReport2idFix={}
    with open(pathBugFixes) as f:
        idBugReport2idFix = json.load(f)

    with open(pathAnnotation) as f:
        df = json.load(f)
        for commitFix in df:
            for item in df[commitFix]:
                if(1<len(item["revisions"])):
                    if(not item["filePath"] in historyBugFile):
                        historyBugFile[item["filePath"]]={}
                    #ここでバグレポートidを入れる
                    idBugReport=""
                    for key in idBugReport2idFix:
                        if(idBugReport2idFix[key]["hash"]==commitFix):
                            idBugReport=key.split('_')[0]
                    if(not idBugReport in historyBugFile[item["filePath"]]):
                        historyBugFile[item["filePath"]][idBugReport]={}
                    if(not commitFix in historyBugFile[item["filePath"]][idBugReport]):
                        historyBugFile[item["filePath"]][idBugReport][commitFix]=[]
                    revisions=[i for i in item["revisions"] if i!=commitFix]
                    historyBugFile[item["filePath"]][idBugReport][commitFix].extend(revisions)
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
        pathInput="annotations.json"
    return pathInput

def getPathOutput(path):
    pathOutput=""
    if(0<len(path)):
        pathOutput=path
    else:
        pathOutput="bugs.json"
    return pathOutput


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--pathAnnotation', type=str, default="")
    parser.add_argument('--pathBugFixes', type=str, default="")
    parser.add_argument('--pathOutput', type=str, default="", help="dest")

    args = parser.parse_args()
    pathAnnotation = getPathInput(args.pathAnnotation)
    pathBugFixes = getPathInput(args.pathBugFixes)
    pathOutput = getPathOutput(args.pathOutput)

    reformat(pathAnnotation, pathBugFixes, pathOutput)