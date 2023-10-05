import time
import threading
from flask import Flask, jsonify
from helpers.constants.definitions import MAC_ADDR_LEN
from helpers.parsers.tcp_to_json_parser import tcp_json_parser
from scripts.get_histogram_traffic import get_usr_histogram_trf
from scripts.get_recent_traffic import get_usr_trf_recent
from scripts.get_user import get_usr_data
from scripts.redis_connection import redis_db
from scripts.tcp_parser import tcp_parser
from scripts.worker import worker

app = Flask(__name__)


@app.route("/")
def index():
    all_hashes = redis_db.keys("*")
    users = [hashes for hashes in all_hashes if len(hashes) <= MAC_ADDR_LEN]
    user_list = []

    for user_mac in users:
        user = get_usr_data(user_mac)
        usr_trf = get_usr_trf_recent(user_mac)
        user["apps"] = usr_trf
        user_list.append(user)
    return jsonify(user_list)


@app.route("/<path:mac>", methods=["GET"])
def get_user_by_mac(mac):
    mac = mac.replace("-", ":")
    user = get_usr_data(mac)
    usr_trf = get_usr_trf_recent(mac)
    user["apps"] = usr_trf
    return jsonify(user)


@app.route("/<path:mac>/history", methods=["GET"])
def get_user_history_by_mac(mac):
    mac = mac.replace("-", ":")
    user = get_usr_data(mac)
    usr_trf = get_usr_histogram_trf(mac)
    user["apps"] = usr_trf
    return jsonify(user)


class WorkerThread(threading.Thread):
    def run(self):
        print("[info] : worker thread running...")
        while True:
            uuid = int(time.time())
            out_file = tcp_json_parser(uuid)
            worker(out_file)
            time.sleep(15)


class ParserThread(threading.Thread):
    def run(self):
        print("[info] : tcp parser thread running...")
        while True:
            tcp_parser()
            pass


if __name__ == "__main__":
    th1 = WorkerThread()
    th2 = ParserThread()
    th1.start()
    th2.start()
    app.run(
        host="localhost",
        port=6000,
        debug=True,
        use_reloader=False,
    )
