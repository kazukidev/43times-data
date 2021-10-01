import os
import json
import pathlib
import requests
import glob
import re
import datetime

# Get timestamp
#now = datetime.datetime.now()

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


# fetch and write the contents as json file
response = requests.get(os.getenv("API_URL", "http://localhost:3000/api/today/property")).json()

Year =  response['date']['year'] 
Month = response['date']['month']

daily_dirname = './data/daily/' + Year + '/' + Month
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


def getMonthly(symbol):
    response = requests.get(f'{os.getenv("SPREADSHEET_URL")}?type={symbol}').json()
    month_dirname = f'./data/monthly/{Year}/{Month}' 
    pathlib.Path(month_dirname).mkdir(parents=True, exist_ok=True)
    with open(f'{month_dirname}/{symbol}.json', 'w') as output:
        json.dump(response, output, indent=2, sort_keys=True)


symbols = ['DJI', 'IXIC', 'INX', 'RUT', 'NI225', '2801']
for symbol in symbols:
    getMonthly(symbol)

with open(f'./data/monthly/{Year}/{Month}/symbols.json', 'w') as output:
    js = []
    for s in symbols:
        obj = {}
        obj["name"] = s
        js.append(obj)
    json.dump(js, output, indent=2, sort_keys=True)
