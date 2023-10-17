import json
import os
from helpers.parsers._parser import parse_data_stream
from scripts.redis_connection import redis_db


def worker(out_file):
    """
    @param out_file (str)    : name of output file after tcp parser
    """
    (users, pkts) = parse_data_stream(out_file)
    for user in users:
        for hash_key, data in user.items():
            existing_user = redis_db.hget(hash_key, "data")
            if existing_user is not None:
                continue
            else:
                data = json.dumps(data)
                redis_db.hset(str(hash_key), mapping={'data': data})

    for pkt in pkts:
        for hash_key, data in pkt.items():
            existing_pkt = redis_db.hget(hash_key, "data")
            if existing_pkt is not None:
                existing_pkt = json.loads(existing_pkt)  # Load JSON if it exists
                data["bytes_ttl"] += int(existing_pkt.get("bytes_ttl", 0))
                data["bytes_up"] += int(existing_pkt.get("bytes_up", 0))
                data["bytes_dn"] += int(existing_pkt.get("bytes_dn", 0))
                data["pkts_ttl"] += int(existing_pkt.get("pkts_ttl", 0))
                data["pkts_up"] += int(existing_pkt.get("pkts_up", 0))
                data["pkts_dn"] += int(existing_pkt.get("pkts_dn", 0))

            data = json.dumps(data)
            redis_db.hset(str(hash_key), mapping={'data': data})

    print("data stream stored!")
