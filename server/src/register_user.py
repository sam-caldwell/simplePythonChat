import json

def register_user(request, auth_secret_file):
    """
        Registration API (POST: /api/v1/register)

        Allows a user to register their handle and get a UserId to post chat messages.

        :param request:
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
    secret,userHandle="",""
    try:
        body = request.json
        if "secret" in body:
            secret=body["secret"]
        else:
            return json.dumps({"status":"UNAUTHORIZED"}), 401
        if "userHandle" in body:
            userHandle=body["userHandle"]
        else:
            return json.dumps({"status":"Bad Request"}), 400
    except Exception as e:
        print(f"Error(parse): {e}")
        return json.dumps({"status": "BAD_REQUEST"}), 400

    try:
        # Inspect secret to authenticate operation.
        with open(auth_secret_file,"r") as f:
            if f.read() != secret:
                return json.dumps({"status":"FORBIDDEN"}), 403
    except Exception as e:
        print(f"Error(auth): {e}")
        return json.dumps({"status": "INTERNAL SERVER ERROR"}), 500
