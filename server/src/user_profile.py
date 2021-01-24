from os.path import join


def user_profile(user_data, user_id):
    """
        Return a filename for the user's profile.

        :param user_data: string
        :param user_id: string
        :return: string
    """
    return join(user_data, f"{user_id}.dat")
