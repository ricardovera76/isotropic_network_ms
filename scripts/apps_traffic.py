import json
from helpers.handlers.apps_names import applications, get_app_name, get_technical_app_name
from scripts.redis_connection import redis_db
from helpers.constants.definitions import APP_FILE, URL


def apps_trf(target_app=""):
    """
    @param target_app (str)         : name of the target app, if not given, default value "" [optional]
    @return app_list  (list[dict])  : list of all app inf with traffic as a dictionary
    """
    app_list = {}
    applications_list = applications(APP_FILE, URL)
    # list to store the app data sorted by the "last_seen" field
    app_data = []
    # Retrieve all keys matching the pattern "app:*" or "app:<target_app>:" from Redis
    app_technical_name = get_technical_app_name(applications_list, target_app) if "" != target_app else "*"
    all_apps = redis_db.keys(f"app:{app_technical_name}:*")

    for app_key in all_apps:
        app_name = app_key.split(":")[1]
        data = json.loads(redis_db.get(app_key))
        # step 1 : if name not in app list save app name in app list
        if app_name not in app_list:
            app_list[app_name] = data
        else:
            app_list[app_name].append(data[0])

    # for every app in app list print all
    for app_name, app_trf in app_list.items():
        total_rate = 0
        for trf in app_trf:
            total_rate += trf["rate_ttl"]
        app_data.append({
            "name": get_app_name(applications_list, app_name),
            "totalRate": total_rate
        })

    top_apps = sorted(app_data, key=lambda x: x["totalRate"], reverse=True)

    return top_apps