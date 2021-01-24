import uuid
from src.hash_string import hash_string

def generate_auth_token():
    """
        Generate an auth token (sha256 hash) of a UUID4.
        :return: str
    """
    return hash_string(str(uuid.uuid4()))