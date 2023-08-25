from helpers._parser import parse_data_stream
from helpers.redis_connection import redis_db


def worker():
    data = parse_data_stream()
    for d in data:
        key = f'{d["application"]}-{d["time_stamp"]}'
        redis_db.hset(key, mapping=d)
        print("data stream stored!")


