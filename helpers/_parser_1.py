import json
import matplotlib.pyplot as plt
from helpers.apps_names import applications
from datetime import datetime
from helpers.cache_compare import cache_diff
from helpers.flow_parser import flow_parser
from helpers.get_users_data import get_users
from helpers.get_pkt_data import get_pkt


APP_FILE = "applications.json"
URL = "https://informatics.netify.ai/api/v2/lookup/applications"

def parse_data_stream():
    source_file = "/tmp/out.json"
    cache_file = "/tmp/cache.json"
    diff_file = "/tmp/diff.json"

    app_list = applications(APP_FILE, URL)

    digest_lst_all = []

    # get diff of data streams [✅]
    cache_diff(cache_file, source_file, diff_file)

    # get all digests (uniques) [✅]
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

    # get all flows and flows_st_pr [✅]
    dig_flow_app = flow_parser(diff_file, unique_digests, "flow")
    dig_flow_pkt = flow_parser(diff_file, unique_digests, "st_pr")

    # get unique list of users [✅]
    # within all those digests get unique mac and ip [✅]
    users_list = get_users(dig_flow_app, app_list)
    users = [
        {
            f"{user['mac']}": user
        }
        for user in users_list
    ]

    # get unique list of packets flows [✅]
    # within all those digests get the packets and bytes [✅]
    # within all those digests get app [✅]
    pkt_list = get_pkt(dig_flow_pkt)
    pkts = [
        {
            f'{pkt["digest"]}':pkt
        }
        for pkt in pkt_list
    ]

    return (users, pkts)