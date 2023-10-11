import time
import threading
from flask import Flask, jsonify
from helpers.constants.definitions import MAC_ADDR_LEN
from helpers.parsers.tcp_to_json_parser import tcp_json_parser
from scripts.app_histogram import app_history
from scripts.app_traffic import app_trf
from scripts.apps_traffic import apps_trf
from scripts.device_data import device_data
from scripts.device_histogram import device_histogram
from scripts.device_traffic import device_recent_trf
from scripts.redis_connection import redis_db
from scripts.sys_traffic import system_trf
from scripts.tcp_parser import tcp_parser
from scripts.worker import worker

app = Flask(__name__)


@app.route("/devices")
def get_all_current_devices():
    all_hashes = redis_db.keys("*")
    devices = [hashes for hashes in all_hashes if len(hashes) <= MAC_ADDR_LEN]
    device_list = []

    for device_mac in devices:
        device = device_data(device_mac)
        usr_trf = device_recent_trf(device_mac)
        device["apps"] = usr_trf
        device_list.append(device)
    return jsonify(device_list)


@app.route("/device/<path:mac>", methods=["GET"])
def get_device_by_mac(mac):
    mac = mac.replace("-", ":")
    device = device_data(mac)
    dev_trf = device_recent_trf(mac)
    device["apps"] = dev_trf
    return jsonify(device)


@app.route("/device/<path:mac>/history", methods=["GET"])
def get_user_history_by_mac(mac):
    mac = mac.replace("-", ":")
    device = device_data(mac)
    dev_trf = device_histogram(mac)
    device["apps"] = dev_trf
    return jsonify(device)

@app.route("/apps", methods=["GET"])
def get_top_apps():
    data = apps_trf()
    return jsonify(data)

@app.route("/app/<path:app_name>", methods=["GET"])
def get_app_top_data(app_name):
    app = app_trf(app_name)
    return jsonify(app)

@app.route("/app/<path:app_name>/history", methods=["GET"])
def get_app_histogram(app_name):
    app = app_history(app_name)
    return jsonify(app)

@app.route("/system", methods=["GET"])
def get_sys_rate():
    sys_rate = system_trf()
    return jsonify(sys_rate)

class WorkerThread(threading.Thread):
    def run(self):
        print("[info] : worker thread running...")
        while True:
            time.sleep(15)
            uuid = int(time.time())
            out_file = tcp_json_parser(uuid)
            worker(out_file)


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
        use_reloader=True,
    )
