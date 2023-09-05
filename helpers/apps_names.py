import json
import requests
import os


def applications(APP_FILE,URL):
    if os.path.exists(APP_FILE):
        with open(APP_FILE) as localfile:
            data = json.load(localfile)
    else:
        params = {
            "settings_data_format": "objects",
            "settings_limit": 5000,
        }
        headers = {
            "content-type": "application/json",
        }
        response = requests.get(URL, data=json.dumps(params), headers=headers)
        # Save to cache
        with open(APP_FILE, mode="w") as localfile:
            json.dump(response.json()["data"], localfile)
        data = response.json()["data"]

    return data
