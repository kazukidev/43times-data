import os
import json
import pathlib
import requests
import glob
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


# fetch and write the contents as json file
response = requests.get(os.getenv("API_URL", "http://localhost:3000/api/today/property")).json()
daily_dirname = './data/daily/' + response['date']['year'] + '/' + response['date']['month']
filename = response['date']['date'] + ".json"
pathlib.Path(daily_dirname).mkdir(parents=True, exist_ok=True)
with open(daily_dirname + '/' + filename, 'w') as output:
    json.dump(response, output, sort_keys=True)

# fetch and write the list of date as json file
with open("data/daily.json", 'w') as output:
    daily = []
    for x in sorted(glob.glob("data/daily/**/*.json", recursive=True), key=natural_keys):
        _, _, year, month, date = os.path.splitext(x)[0].split("/")
        daily.append({"year": int(year), "month": int(month), "date": int(date)})
    json.dump(daily, output, indent=4, sort_keys=True)
