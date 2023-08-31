import json
from helpers._parser_1 import parse_data_stream
from helpers.redis_connection import redis_db

MAC_ADDR_LEN = 17


def worker():
    # get newly updated data from redis [✅]
    # Retrieve all keys (hashes) from Redis [✅]
    all_hashes = redis_db.keys("*")
    users = [hashes for hashes in all_hashes if len(hashes) <= MAC_ADDR_LEN]
    pkts = [hashes for hashes in all_hashes if len(hashes) > MAC_ADDR_LEN]
    user_list = []
    # make correlation [✅]
    for user_hash in users:
        user = json.loads(redis_db.hget(user_hash, "data"))
        user["applications"] = []
        for app in user["apps"]:
            appl = redis_db.hget(app[0], "data")
            appl = json.loads(appl)
            user["applications"].append(appl)
        user_list.append(user)
    # print(user_list)
    return (user_list)


worker()
