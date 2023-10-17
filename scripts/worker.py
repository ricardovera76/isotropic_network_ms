import json
import os
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
                redis_db.hmset(f"device:{str(hash_key)}",data)

    for pkt in pkts:
        for hash_key, data in pkt.items():
            pkt_exists = redis_db.exists(f"pkt:{str(hash_key)}")
            # if pkt_exists:
                # pkts_up_old = redis_db.hmget(f"pkt:{str(hash_key)}", "pkts_up")
                # pkts_dn_old = redis_db.hmget(f"pkt:{str(hash_key)}", "pkts_dn")
                # pkts_ttl_old = redis_db.hmget(f"pkt:{str(hash_key)}", "pkts_ttl")
                # data["pkts_ttl"] = str(int(data["pkts_ttl"]) + int(pkts_ttl_old))
                # data["pkts_up"] = str(int(data["pkts_up"]) + int(pkts_up_old))
                # data["pkts_dn"] = str(int(data["pkts_dn"]) + int(pkts_dn_old))

            redis_db.hmset(f"pkt:{str(hash_key)}", data)

    print("data stream stored!")
