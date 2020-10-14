# 取得するやつ
# key: Jenkins-27380とか
# creationdate
# resolutiondate

import requests, os

owner = "google"
repository = "guava"
url = 'https://api.github.com/repos/' + owner + '/' + repository + '/issues' +  "?per_page=1000" + "&page=2"
print(url)

res = requests.get(url)

pathFile = "text.json"
with open(pathFile, mode='w', encoding="utf_8") as f:
    f.write(res.text)
