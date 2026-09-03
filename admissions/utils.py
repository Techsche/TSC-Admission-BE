import hashlib
import secrets


def generate_application_token():
    return secrets.token_urlsafe(48)


def hash_application_token(token):
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()