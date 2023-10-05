import json
from scripts.redis_connection import redis_db
from helpers.constants.definitions import MAC_ADDR_LEN


def get_usr_trf_recent(target_mac):
    """
    @param target_mac (string)          : mac address of user to get recent traffic per-app

    @return app_list (list[dict])       : list of all app inf with traffic as a dictionary
    """
    # Initialize an empty list to store matching hash keys
    # Dictionary to store the most recent digest object for each app_name
    app_last_seen = {}  # {"netify.x_app_name":123456789 (unix of last time of app)}

    all_digests = [data for data in redis_db.keys("*") if len(data) > MAC_ADDR_LEN]

    for digest in all_digests:
        current_digest = json.loads(redis_db.hget(digest, "data"))
        if target_mac == current_digest["mac_addr"]:
            # Check if the app_name is repeated and compare last seen timestamp, get most recent traffic for a given app
            app_name = current_digest["app_name"]
            last_seen = current_digest["last_seen"]
            if app_name in app_last_seen:
                if last_seen > app_last_seen[app_name]["last_seen"]:
                    app_last_seen[app_name] = current_digest
            else:
                app_last_seen[app_name] = current_digest

    return list(app_last_seen.values())
