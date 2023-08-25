import matplotlib.pyplot as plt
import json
import requests
import os
from datetime import datetime

APP_FILE = "applications.json"
URL = "https://informatics.netify.ai/api/v2/lookup/applications"
INTERVAL = 15


def unix_to_date(unix_time_ms):
    timestamp_in_milliseconds = unix_time_ms
    timestamp_in_seconds = timestamp_in_milliseconds / 1000
    normal_date = datetime.utcfromtimestamp(timestamp_in_seconds).strftime(
        "%Y-%m-%d_%H:%M:%S"
    )
    return normal_date


def parse_data_stream():
    source_file = "/tmp/out.json"

    app_list = applications()

    interval = 0
    interval_bytes_dn = 0
    interval_bytes_up = 0
    first_seen = 0
    last_seen = 0
    total_bytes_dn = 0
    total_bytes_up = 0
    mapping = {}
    parent = {}
    bps_dn = []
    bps_up = []
    parent["netify.established"] = {
        "label": "Established",
        "bytes_dn": 0,
        "bytes_up": 0,
    }
    response = []

    with open(source_file) as file:
        for line in file:
            print(line)
            
        return "response"


def applications():
    app_dict = {}
    # Get cached file
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
        print(response.json()["data"])
        with open(APP_FILE, mode="w") as localfile:
            json.dump(response.json()["data"], localfile)
        data = response.json()["data"]
    for application in data:
        app_dict[application["id"]] = application

    return app_dict

