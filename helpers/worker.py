import json
from helpers._parser_1 import parse_data_stream
from helpers.redis_connection import redis_db


def worker():
    (users, pkts) = parse_data_stream()
    # save data to redis [✅]
    for user in users:
        for hash_key, data in user.items():
            existing_user = redis_db.hget(hash_key, "data")
            if existing_user != None:
                existing_user = json.loads(existing_user)
                for app in data['apps']:
                    existing_user['apps'].append(app)
                existing_user = json.dumps(existing_user)
                redis_db.hset(str(hash_key), mapping={'data': existing_user})
            else:
                data = json.dumps(data)
                redis_db.hset(str(hash_key), mapping={'data': data})
            print("data stream stored!")
    for pkt in pkts:
        for hash_key, data in pkt.items():
            data = json.dumps(data)
            redis_db.hset(str(hash_key), mapping={'data': data})
            print("data stream stored!")
