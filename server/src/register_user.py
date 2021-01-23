
def register_user(request):
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


    print("register_user")
    return "OK",200