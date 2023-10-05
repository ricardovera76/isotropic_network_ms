import json
from helpers.handlers.apps_names import applications
from helpers.handlers.cache_compare import cache_diff
from helpers.parsers.flow_parser import flow_parser
from helpers.parsers.get_flow_data import get_flows
from helpers.parsers.get_user_data import get_user
from helpers.parsers.get_flow_stats import get_stats
from helpers.constants.definitions import DIR_FILE, APP_FILE, URL

def parse_data_stream(source_file):
    """
    @param source_file (string)             : name of source file after tcp parser
    
    @return (user, apps) (tuple)            : tuple of list of all users as dictionaries and list of all apps flows as dictionaries    
    """
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
    
    users_list = get_user(dig_flow_app)
    users = [
        {
            f"{user['mac']}": user
        }
        for user in users_list
    ]
    
    # gets flows stats of each app usage
    pkts = get_stats(dig_flow_pkt)
    
    apps_list = get_flows(dig_flow_app, pkts)
    apps = [
        {
            f'{app["digest"]}':app
        }
        for app in apps_list
    ]

    return (users, apps)