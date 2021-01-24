import json
from src.user_hash import user_hash
from src.user_profile import user_profile


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
