import json
from helpers.parsers._parser import parse_data_stream
from scripts.redis_connection import redis_db


def worker(out_file):
    """
    @param out_file (str)    : name of output file after tcp parser
    """
    (decives, pkts) = parse_data_stream(out_file)
    for device in decives:
        for hash_key, data in device.items():
            device_exist = redis_db.exists(f"device:{hash_key}")
            if device_exist:
                continue
            else:
                redis_db.hmset(f"device:{str(hash_key)}", data)

    repeated_apps = {}
    for pkt in pkts:
        for hash_key, data in pkt.items():
            app_name = data["app_name"]
            mac = data["mac_addr"]
            mac_data = {
                "rate_up": data["rate_up"],
                "rate_dn": data["rate_dn"],
                "rate_ttl": float(data["rate_up"]) + float(data["rate_dn"]),
                "last_seen": data["last_seen"],
            }
            if app_name not in repeated_apps:
                repeated_apps[app_name] = {
                    "app_name": app_name,
                    "mac_list": {f"{mac}": [mac_data]},
                }

            if mac not in repeated_apps[app_name]["mac_list"]:
                repeated_apps[app_name]["mac_list"][mac] = [mac_data]
                
    for app_name, app_data in repeated_apps.items():
        for mac, mac_data in app_data["mac_list"].items():
            redis_key = f"app:{app_name}:{mac}"
            redis_db.set(redis_key, json.dumps(mac_data))

    print("[info] : data stream stored!")
