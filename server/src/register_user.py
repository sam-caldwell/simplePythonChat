import json
from src.generate_user_id import generate_user_id
from src.create_user_profile import create_user_profile


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
