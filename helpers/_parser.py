import json
import matplotlib.pyplot as plt
from helpers.apps_names import applications
from datetime import datetime
from helpers.cache_compare import cache_diff
from helpers.flow_parser import flow_parser
from helpers.get_users_data import get_users
from helpers.get_pkt_data import get_pkt

DIR_FILE = "/tmp/"
APP_FILE = f"{DIR_FILE}applications.json"
URL = "https://informatics.netify.ai/api/v2/lookup/applications"

def parse_data_stream():
    source_file = f"{DIR_FILE}out.json"
    cache_file = f"{DIR_FILE}cache.json"
    diff_file = f"{DIR_FILE}diff.json"

    app_list = applications(APP_FILE, URL)

    digest_lst_all = []

    cache_diff(cache_file, source_file, diff_file)

    with open(diff_file) as file:
        digest_lst_all = [
            json.loads(line)["flow"]["digest"]
            for line in file
            if json.loads(line).get("flow") is not None
        ]
    unique_digests = []
    [
        unique_digests.append(item)
        for item in digest_lst_all
        if item not in unique_digests
    ]

    dig_flow_app = flow_parser(diff_file, unique_digests, "flow")
    dig_flow_pkt = flow_parser(diff_file, unique_digests, "st_pr")

    users_list = get_users(dig_flow_app, app_list)
    users = [
        {
            f"{user['mac']}": user
        }
        for user in users_list
    ]

    pkt_list = get_pkt(dig_flow_pkt)
    pkts = [
        {
            f'{pkt["digest"]}':pkt
        }
        for pkt in pkt_list
    ]

    return (users, pkts)