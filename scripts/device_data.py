import json
from scripts.device_traffic import device_recent_trf
from scripts.redis_connection import redis_db


def device_data(mac):
    """
    @param mac      (string)    : mac address of device

    @return device    (dict)      : dictionary of device data
    """
    device = redis_db.hgetall(f"device:{mac}")
    device_trf = device_recent_trf(mac)
    # # get current rate 4 e/app added up to ttl device rate
    device_up_rate = 0
    device_dn_rate = 0
    device_ttl_rate = 0
    device_last_seen = 0
    for app_trf in device_trf:
        if device_last_seen <= int(app_trf["last_seen"]):
            device_last_seen = int(app_trf["last_seen"])
        device_up_rate += float(app_trf["rate_up"])
        device_dn_rate += float(app_trf["rate_dn"])
        device_ttl_rate += float(app_trf["rate_up"]) + float(app_trf["rate_dn"])
    device["rate_up"] = device_up_rate
    device["rate_dn"] = device_dn_rate
    device["rate_ttl"] = device_ttl_rate
    device["last_seen"] = int(device_last_seen)//1000
    return device