from scripts.device_data import device_data
from scripts.redis_connection import redis_db
from helpers.constants.definitions import MAC_ADDR_LEN


def system_trf():
    all_hashes = redis_db.keys("*")
    devices = [hashes for hashes in all_hashes if len(hashes) <= MAC_ADDR_LEN]
    device_trf_list = []
    sys_trf_up = 0
    sys_trf_dn = 0
    sys_trf_ttl = 0
    sys_timestamp = 0

    for device_mac in devices:
        device = device_data(device_mac)
        device_trf_list.append(
            {
                "rate_up": device["rate_up"],
                "rate_dn": device["rate_dn"],
                "rate_ttl": device["rate_ttl"],
                "timestamp": device["last_seen"]
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
