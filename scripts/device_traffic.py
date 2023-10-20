import json
from scripts.redis_connection import redis_db


def device_recent_trf(target_mac):
    """
    @param target_mac (string)          : mac address of device to get recent traffic per-app

    @return app_list (list[dict])       : list of all app inf with traffic as a dictionary
    """
    app_list = {}
     # list to store the app data sorted by the "last_seen" field
    app_data = []
    # Retrieve all keys matching the pattern "app:*:<target_mac>" from Redis
    all_apps = redis_db.keys(f"app:*:{target_mac}")

    for app_key in all_apps:
        app_data_dict = json.loads(redis_db.get(app_key))[0]
        app_data_dict["app_name"] = app_key.split(":")[1]  # Extract the app name
        app_data.append(app_data_dict)

    app_data.sort(key=lambda x: x.get("last_seen", 0), reverse=True)

    for app_info in app_data:
        app_name = app_info["app_name"]
        app_list[app_name] = app_info

    return list(app_list.values())
