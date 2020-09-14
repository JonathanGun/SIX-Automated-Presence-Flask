import os
from selenium.webdriver.firefox.options import Options
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

import logging
logging.basicConfig(format='[%(asctime)s] - %(message)s', datefmt='%d %b %H:%M:%S', level=logging.INFO)

from presence import presence
message = {
    1: "Invalid password",
    2: "There's currently no class",
    3: "Presence form not opened yet",
    4: "Presence form filled successfully",
    5: "Presence form already filled",
}

option = Options()
option.add_argument("--headless")

@app.route("/", methods=["POST"])
def main():
    if not request.json or "credentials" not in request.json:
        abort(400)
    args = {
        "username": request.json["credentials"]["username"],
        "password": request.json["credentials"]["password"],
        "logging": app.logger
    }
    app.logger.info("Username: " + args["username"])

    code, classname = presence(**args)
    app.logger.info("Finished with code: " + str(code) + " | " + message[code])

    return jsonify({
        "code": code,
        "class": classname,
        "message": message[code],
    }), 200

if __name__ == "__main__":
    app.run(debug=False)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    option.binary_location = os.getenv('FIREFOX_BIN')
    option.add_argument('--disable-gpu')
    option.add_argument('--no-sandbox')
