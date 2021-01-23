from flask import Flask

"""
    simplePythonChat API
    (c) 2021 Sam Caldwell, Jenny Faraday.  See LICENSE.txt
    
    This is a simple Flask API to facilitate chat between
    users.

"""

APP_VERSION = "1.0"
app = Flask(__name__)

def noop():
    return "OK", 200


@app.route('/')
def hello_world():
    message, code = noop()
    return message, code


@app.route('/api/v1/register', methods=["GET", "POST"])
def api_v1_register():
    message, code = register_user()
    return message, code


@app.route('/api/v1/chat', methods=["GET", "POST"])
def api_v1_chat():
    message, code = noop()
    return message, code


@app.route("/health", methods=["GET"])
def api_v1_health():
    message, code = noop()
    return message, code


@app.route("/version", methods=["GET"])
def api_v1_version():
    return APP_VERSION, 200


if __name__ == '__main__':
    app.run()
