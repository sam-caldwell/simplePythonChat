"""
    simplePythonChat API
    (c) 2021 Sam Caldwell, Jenny Faraday.  See LICENSE.txt
    
    This is a simple Flask API to facilitate chat between
    users.

"""
from os.path import join
from os.path import dirname
from flask import Flask, request
from src.register_user import register_user
from src.query_user import query_user
from src.chat_send import chat_send
from src.chat_recv import chat_recv

APP_VERSION = "1.0"
DATA_ROOT = join(dirname(__file__), "data")
AUTH_SECRET_FILE = join(DATA_ROOT, "secret.dat")
app = Flask(__name__)


@app.route('/')
def hello_world():
    """
        Default Route.  Return only http/200 OK.
        :return: string, int
    """
    return "OK", 200


@app.route('/api/v1/register', methods=["GET", "POST"])
def api_v1_register():
    """
        User Registration endpoint.
        :return: string, int
    """
    if request.method == "POST":
        return register_user(request, AUTH_SECRET_FILE)
    elif request.method == "GET":
        return query_user(request)
    else:
        return "METHOD NOT SUPPORTED", 405


@app.route('/api/v1/chat', methods=["GET", "POST"])
def api_v1_chat():
    """
        Message Exchange (send, receive) endpoint
        :return: string, int
    """
    if request.method == "POST":
        return chat_send(request)
    elif request.method == "GET":
        return chat_recv(request)
    else:
        return "METHOD NOT SUPPORTED", 405


@app.route("/health", methods=["GET"])
def api_v1_health():
    """
        Healthcheck endpoint
        :return: string, int
    """
    return "OK", 200


@app.route("/version", methods=["GET"])
def api_v1_version():
    """
        Version endpoint
        :return: string, int
    """
    return APP_VERSION, 200


if __name__ == '__main__':
    app.run()
