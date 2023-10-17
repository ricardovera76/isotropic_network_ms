import json
from scripts.redis_connection import redis_db

def device_histogram(target_mac):
    """
    @param target_mac (string)          : mac address of device to get recent traffic per-app

    @return app_list (list[dict])       : list of all app info with traffic as a dictionary
    """

    all_digests = redis_db.keys("pkt:*")

    return [
        redis_db.hgetall(digest)
        for digest in all_digests
        if target_mac == redis_db.hgetall(digest)["mac_addr"]
    ]
