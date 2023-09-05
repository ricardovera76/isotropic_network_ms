import json
from helpers._parser import parse_data_stream
from helpers.redis_connection import redis_db


def worker():
    (users, pkts) = parse_data_stream()
    apps = []
    apps_hash = {}
    for user in users:
        for hash_key, data in user.items():
            existing_user = redis_db.hget(hash_key, "data")
            if existing_user != None:
                existing_user = json.loads(existing_user)
                for app in data['apps']:
                    existing_user['apps'].append(app)
                    apps.append(app)
                existing_user = json.dumps(existing_user)
                redis_db.hset(str(hash_key), mapping={'data': existing_user})
            else:
                data = json.dumps(data)
                redis_db.hset(str(hash_key), mapping={'data': data})
    for item in apps:
        digest, app_name = item
        if digest not in apps_hash:
            apps_hash[digest] = app_name
    for pkt in pkts:
        for hash_key, data in pkt.items():
            data["app_name"] = apps_hash.get(hash_key) or "Unknown"
            data = json.dumps(data)
            redis_db.hset(str(hash_key), mapping={'data': data})
    print("data stream stored!")
