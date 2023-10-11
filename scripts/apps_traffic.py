import json
from helpers.handlers.apps_names import applications, get_app_name
from scripts.redis_connection import redis_db
from helpers.constants.definitions import APP_FILE, MAC_ADDR_LEN, URL


def apps_trf():
    """
    @return app_list (list[dict])       : list of all app inf with traffic as a dictionary
    """
    # Initialize an empty list to store matching hash keys
    # Dictionary to store the most recent digest object for each app_name
    app_last_seen = {}  # {"netify.x_app_name":123456789 (unix of last time of app)}
    applications_list = applications(APP_FILE, URL)
    app_list = []

    all_digests = [data for data in redis_db.keys("*") if len(data) > MAC_ADDR_LEN]

    for digest in all_digests:
        current_digest = json.loads(redis_db.hget(digest, "data"))
        app_name = current_digest["app_name"]
        last_seen = current_digest["last_seen"]
        if app_name in app_last_seen:
            if last_seen > app_last_seen[app_name]["last_seen"]:
                app_last_seen[app_name] = current_digest
        else:
            app_last_seen[app_name] = current_digest

    apps = list(app_last_seen.values())
    for app in apps:
        app_name = get_app_name(applications_list, app['app_name'])
        total_rate = int(app['rate_up']) + int(app['rate_dn'])
        app_list.append({
            "name": app_name,
            "totalRate": total_rate
        })
        
    top_apps = sorted(app_list, key=lambda x: x["totalRate"], reverse=True)
    
    return top_apps
