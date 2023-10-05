import json
from scripts.redis_connection import redis_db
from helpers.constants.definitions import MAC_ADDR_LEN


def get_usr_histogram_trf(target_mac):
    """
    @param target_mac (string)          : mac address of user to get recent traffic per-app

    @return app_list (list[dict])       : list of all app info with traffic as a dictionary
    """

    all_digests = [data for data in redis_db.keys("*") if len(data) > MAC_ADDR_LEN]

    return [
        json.loads(redis_db.hget(digest, "data"))
        for digest in all_digests
        if target_mac == json.loads(redis_db.hget(digest, "data"))["mac_addr"]
    ]
