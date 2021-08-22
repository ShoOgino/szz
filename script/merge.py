# reports.jsonを読んで、
import argparse
import json 
from datetime import datetime as dt
from datetime import timedelta as td

def test(pathInput, pathOutput):
    merged={}
    for i in range(32):
        with open(pathInput+"/result"+str(i)+"/annotations.json") as f:
            df = json.load(f)
            for key in df:
                if(key not in merged):
                    merged[key]=df[key]
    with open(pathOutput, 'w') as f:
        json.dump(merged, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Convert a git log output to json.""")
    parser.add_argument('--pathInput', type=str, default="")
    parser.add_argument('--pathOutput', type=str, default="", help="dest")

    args = parser.parse_args()
    pathInput = args.pathInput
    pathOutput = args.pathOutput

    test(pathInput, pathOutput)