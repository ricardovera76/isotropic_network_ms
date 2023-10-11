import json
from helpers.handlers.apps_names import applications, get_app_name
from scripts.redis_connection import redis_db
from helpers.constants.definitions import APP_FILE, MAC_ADDR_LEN, URL


def app_history(target_app):
    """
    @param target_mac (string)          : mac address of user to get recent traffic per-app

    @return app_list (list[dict])       : list of all app info with traffic as a dictionary
    """

    all_digests = [data for data in redis_db.keys("*") if len(data) > MAC_ADDR_LEN]

    applications_list = applications(APP_FILE, URL)

    app_histogram = [
        json.loads(redis_db.hget(digest, "data"))
        for digest in all_digests
        if target_app
        == get_app_name(
            applications_list, json.loads(redis_db.hget(digest, "data"))["app_name"]
        )
    ]

    return [
        {
            "name": get_app_name(applications_list, history["app_name"]),
            "totalRate": int(history["rate_up"]) + int(history["rate_dn"]),
            "timestamp": int(history["last_seen"]//1000)
        }
        for history in app_histogram
    ]
