import json
from scripts.get_recent_traffic import get_usr_trf_recent
from scripts.redis_connection import redis_db


def get_usr_data(mac):
    """
    @param mac      (string)    : mac address of user

    @return user    (dict)      : dictionary of user data
    """
    user = json.loads(redis_db.hget(mac, "data"))
    usr_trf = get_usr_trf_recent(mac)
    # get current rate 4 e/app added up to ttl usr rate
    usr_up_rate = 0
    usr_dn_rate = 0
    for app_trf in usr_trf:
        usr_up_rate += app_trf["rate_up"]
        usr_dn_rate += app_trf["rate_dn"]
    user["rate_up"] = usr_up_rate
    user["rate_dn"] = usr_dn_rate
    return user