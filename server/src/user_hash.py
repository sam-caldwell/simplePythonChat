import hashlib


def user_hash(input_string):
    """
        sha256 hash of a given string.

        :param input_string: str
        :return: str (hex)
    """
    m = hashlib.sha256()
    m.update(input_string.encode('ASCII'))
    return m.hexdigest()
