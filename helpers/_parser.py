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
            j = json.loads(line)
            if "type" in j and j["type"] == "flow":
                # here get ip, port, dns host name, protocols, last seen, first seen, mac
                # print(j)
                # ex : 1,2
                app = {"tag": "netify.unknown", "label": "Unknown"}
                id = j["flow"]["detected_application"]
                if app_list.get(int(id)) is not None:
                    app = app_list.get(int(id))

                mapping[j["flow"]["digest"]] = {"application": app}

                if app["tag"] not in parent:
                    parent[app["tag"]] = {
                        "label": app["label"],
                        "bytes_dn": 0,
                        "bytes_up": 0,
                    }
            if "type" in j and (j["type"] == "flow_stats" or j["type"] == "flow_purge"):
                # print(j)
                # gets detection_packets and total packets
                # ex : 3
                if interval == 0:
                    interval = j["flow"]["last_seen_at"] / 1000

                if (interval + 15) > j["flow"]["last_seen_at"] / 1000:
                    if j["flow"]["other_bytes"] > 0 or j["flow"]["local_bytes"] > 0:
                        if interval_bytes_dn > 0:
                            bps_dn.append(round(interval_bytes_dn / INTERVAL, 1))
                        if interval_bytes_up > 0:
                            bps_up.append(round(interval_bytes_up / INTERVAL, 1))
                    interval_bytes_dn = 0
                    interval_bytes_up = 0
                    interval = j["flow"]["last_seen_at"] / 1000

                if first_seen == 0 or first_seen > j["flow"]["last_seen_at"] / 1000:
                    first_seen = int(j["flow"]["last_seen_at"] / 1000)
                if last_seen < j["flow"]["last_seen_at"] / 1000:
                    last_seen = int(j["flow"]["last_seen_at"] / 1000)
                total_bytes_dn += j["flow"]["other_bytes"]
                total_bytes_up += j["flow"]["local_bytes"]
                interval_bytes_dn += j["flow"]["other_bytes"]
                interval_bytes_up += j["flow"]["local_bytes"]
                if j["flow"]["digest"] in mapping:
                    parent[mapping[j["flow"]["digest"]]["application"]["tag"]][
                        "bytes_dn"
                    ] += j["flow"]["other_bytes"]
                    parent[mapping[j["flow"]["digest"]]["application"]["tag"]][
                        "bytes_up"
                    ] += j["flow"]["local_bytes"]
                    parent[mapping[j["flow"]["digest"]]["application"]["tag"]][
                        "time_stamp"
                    ] = unix_to_date(j["flow"]["last_seen_at"])
                else:
                    parent["netify.established"]["bytes_dn"] += j["flow"]["other_bytes"]
                    parent["netify.established"]["bytes_up"] += j["flow"]["local_bytes"]
                    parent["netify.established"]["time_stamp"] = unix_to_date(
                        j["flow"]["last_seen_at"]
                    )
        if interval_bytes_dn > 0:
            bps_dn.append(round(interval_bytes_dn / INTERVAL, 1))
        if interval_bytes_up > 0:
            bps_up.append(round(interval_bytes_up / INTERVAL, 1))

        for p in parent:
            response.append(
                {
                    "time_stamp": str(parent[p]["time_stamp"]).replace(" ", "_"),
                    "application": p,
                    "label": parent[p]["label"],
                    "bytes_dn": str(parent[p]["bytes_dn"]),
                    "bytes_up": str(parent[p]["bytes_up"]),
                }
            )
        return response


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

