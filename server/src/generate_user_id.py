import time
from os.path import exists
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
