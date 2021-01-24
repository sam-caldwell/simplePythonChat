import json
import time
from os.path import join
from os.path import exists
from src.user_hash import user_hash
from src.user_profile import user_profile



def generate_user_id(user_data):
    """
        Generate a user ID using a timestamp and ensure it is
        unique.
        :return: int
    """
    while True:
        user_id = int(time.time() * 1000000)
        if not exists(user_profile(user_data, user_id)):
            return user_id
        print("user_id collision: {user_id}")


def create_user_profile(user_data, user_id, user_handle):
    """
        Create a user profile <root>/data/users/<user_id>.dat file
        Create a user profile <root>/data/users/<handle_hash>.dat file

    :param user_data: string
    :param user_id: string
    :param user_handle: string
    :return: none
    """
    with open(user_profile(user_data, user_hash(user_handle)), "w") as f:
        print("Create the user file (handle hash).")
        f.write(str(user_id))

    with open(user_profile(user_data, user_id), "w") as f:
        print("Create the user file (user_id).")
        f.write(user_hash(user_handle))


def register_user(request, user_data, auth_secret_file):
    """
        Registration API (POST: /api/v1/register)

        Allows a user to register their handle and get a UserId to post chat messages.

        :param request: http flask request
        :param user_data: string (directory)
        :param auth_secret_file: string (path/filename)

        :return: string(json), int
            Success (HTTP/200 OK):
                {
                  "userId": <int>,
                  "authToken": "<string>",
                  "status": "OK"
                }
            Failure (HTTP/400 BAD REQUEST): your request is malformed.
                {
                  "status": "BAD REQUEST"
                }
            Failure (HTTP/401 UNAUTHORIZED): no secret was found in the request
                {
                  "status": "UNAUTHORIZED"
                }
            Failure (HTTP/403 FORBIDDEN): an invalid secret.
                {
                  "status": "FORBIDDEN"
                }
            Failure (HTTP/500 INTERNAL SERVER ERROR): Unhandled exception.
                {
                  "status": "INTERNAL SERVER ERROR"
                }
    """
    secret, user_handle = "", ""
    try:
        body = request.json
        if "secret" in body:
            secret = body["secret"]
        else:
            return json.dumps({"status": "UNAUTHORIZED"}), 401
        if "user_handle" in body:
            user_handle = body["user_handle"]
        else:
            return json.dumps({"status": "Bad Request"}), 400
    except Exception as e:
        print(f"Error(parse): {e}")
        return json.dumps({"status": "BAD_REQUEST"}), 400

    try:
        # Inspect secret to authenticate operation.
        with open(auth_secret_file, "r") as f:
            actual_secret = f.read()
            if actual_secret != secret:
                return json.dumps({"status": "FORBIDDEN"}), 403
        print("registration authentication success")
    except Exception as e:
        print(f"Error(auth): {e}")
        return json.dumps({"status": "INTERNAL SERVER ERROR"}), 500

    # We are authenticated...
    try:
        user_id = generate_user_id(user_data)
        print(f"user_id: {user_id}")

        create_user_profile(user_data, user_id, user_handle)

    except Exception as e:
        print(f"Error(auth): {e}")
        return json.dumps({"status": "INTERNAL SERVER ERROR"}), 500

    return "OK", 200
