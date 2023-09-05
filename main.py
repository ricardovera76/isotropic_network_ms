import time
import threading
from flask import Flask, jsonify
from helpers.worker import worker
from helpers.redis_connection import redis_db
import json
MAC_ADDR_LEN = 17

app = Flask(__name__)


@app.route("/")
def index():
    all_hashes = redis_db.keys("*")
    users = [hashes for hashes in all_hashes if len(hashes) <= MAC_ADDR_LEN]
    user_list = []
    
    for user_hash in users:
        user = json.loads(redis_db.hget(user_hash, "data"))
        user["applications"] = []
        for app in user["apps"]:
            appl = redis_db.hget(app[0], "data")
            appl = json.loads(appl)
            user["applications"].append(appl)
        user_list.append(user)
    return jsonify(user_list)


@app.route('/<string:mac>', methods=['GET'])
def get_user_data(mac_addr):
    user = json.loads(redis_db.hget(mac_addr, "data"))
    user["applications"] = []
    for app in user["apps"]:
        appl = redis_db.hget(app[0], "data")
        appl = json.loads(appl)
        user["applications"].append(appl)
    return jsonify(user)


class WorkerThread(threading.Thread):
    def run(self):
        while True:
            worker()
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
