import os
import time
from selenium.webdriver.firefox.options import Options
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

import logging
logging.basicConfig(format='[%(asctime)s] - %(message)s', datefmt='%d %b %H:%M:%S', level=logging.INFO)

from rq import Queue
from worker import conn

q = Queue(connection=conn)


from presence import presence, results


def myhash(d1, i):
    return str(hash(concat_dict(d1) + str(i)))

def concat_dict(d):
    s = ""
    for key, val in d.items():
        s += str(key)
        try:
            s += map(str, val.to_list())
        except Exception:
            s += str(val)
    return s

option = Options()
option.add_argument("--headless")
exec_path = None

@app.route("/check/<str:token>", methods=["GET"])
def check(token):
    if token in results:
        return jsonify(results[token]), 200
    else:
        return jsonify({"message": "Token is not valid"}), 404

@app.route("/", methods=["POST"])
def main():
    if not request.json or "credentials" not in request.json:
        abort(400)
    args = {
        "username": request.json["credentials"]["username"],
        "password": request.json["credentials"]["password"],
        "logging": app.logger,
        "executable_path": exec_path,
        "options": option,
    }

    app.logger.info("Username: " + args["username"])
    q.enqueue(presence, **args)
    return jsonify({
        "token": myhash(args, time.time()),
    }), 202


if __name__ == "__main__":
    app.run(debug=False)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    option.binary_location = os.getenv('FIREFOX_BIN')
    option.add_argument('--disable-gpu')
    option.add_argument('--no-sandbox')
    exec_path = os.getenv('GECKODRIVER_BIN')
