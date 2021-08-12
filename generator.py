import os
import json
import pathlib
import requests

response = requests.get(os.getenv("API_URL", "http://localhost:3000/api/today/property")).json()

dirname = './data/' + response['date']['year'] + '/' + response['date']['month']
filename = response['date']['date'] + ".json"

pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)

with open(dirname + '/' + filename, 'w') as output:
    json.dump(response, output)
