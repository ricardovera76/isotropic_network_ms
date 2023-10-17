from helpers.constants.definitions import MAC_ADDR_START
from scripts.device_data import device_data
from scripts.redis_connection import redis_db


def system_trf():
    devices = redis_db.keys("device:*")
    device_trf_list = []
    sys_trf_up = 0
    sys_trf_dn = 0
    sys_trf_ttl = 0
    sys_timestamp = 0

    for device_mac in devices:
        device = device_data(device_mac[MAC_ADDR_START:])
        device_trf_list.append(
            {
                "rate_up": float(device["rate_up"]),
                "rate_dn": float(device["rate_dn"]),
                "rate_ttl": float(device["rate_ttl"]),
                "timestamp": int(device["last_seen"]),
            }
        )


    for trf in device_trf_list:
        if sys_timestamp <= trf["timestamp"]:
            sys_timestamp = trf["timestamp"]
        sys_trf_up += trf["rate_up"]
        sys_trf_dn += trf["rate_dn"]
        sys_trf_ttl += trf["rate_ttl"]
        
    return {
        "timestamp": sys_timestamp,
        "sourceRate": sys_trf_up,
        "destRate": sys_trf_dn
    }
