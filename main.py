import time
import threading
from flask import Flask, request, jsonify
from helpers.worker import worker
from helpers.redis_connection import redis_db
import json

app = Flask(__name__)


@app.route("/")
def index():
    """The index route."""
    all_hashes = redis_db.keys('*')  # Retrieve all keys (hashes) from Redis
    hash_data = {}

    for hash_key in all_hashes:
        hash_key = hash_key.decode('utf-8')
        hash_values = redis_db.hgetall(hash_key)
        hash_data[hash_key] = {field.decode('utf-8'): value.decode('utf-8') for field, value in hash_values.items()}
    return jsonify(hash_data)


class WorkerThread(threading.Thread):
    def run(self):
        while True:
            worker()
            print("worker thread")
            time.sleep(15)


if __name__ == "__main__":
    t = WorkerThread()
    t.start()
    app.run(
        host="localhost",
        port=7000,
        debug=True,
        use_reloader=False,
    )
