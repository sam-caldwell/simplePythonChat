import json

def authenticate_global(auth_secret_file, secret):
    """
        Read the auth_secret_file and see if the contents match secret.

        :param auth_secret_file: string
        :param secret: string
        :return: boolean
    """
    with open(auth_secret_file, "r") as f:
        actual_secret = f.read()
        return actual_secret == secret
