import json
from src.hash_string import hash_string
from src.user_profile import user_profile
from src.generate_auth_token import generate_auth_token


def create_user_profile(user_data, user_id, user_handle):
    """
        Create a user profile <root>/data/users/<user_id>.dat file
        Create a user profile <root>/data/users/<handle_hash>.dat file

    :param user_data: string
    :param user_id: string
    :param user_handle: string
    :return: auth_token (sha256 string)
    """
    auth_token=generate_auth_token()
    profile=json.dumps({
        "user_id":user_id,
        "user_handle": hash_string(user_handle),
        "auth_token": auth_token
    },indent=4)

    for fn in [hash_string(user_handle),user_id]:
        with open(user_profile(user_data, fn), "w") as f:
            f.write(profile)
    return auth_token