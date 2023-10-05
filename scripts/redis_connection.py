import redis

redis_db = redis.StrictRedis(host="localhost", port="6379", decode_responses=True)
