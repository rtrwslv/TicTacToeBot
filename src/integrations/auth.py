"""Module for auth."""

import jwt
from config import settings
import time


def sign_jwt(user_id: str) -> str:
    """
    Generate a JSON Web Token (JWT) for a given user ID.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        str: The encoded JWT as a string.

    Raises:
        Exception: If there is an issue with encoding the token.
    """
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token


def decode_jwt(token: str) -> dict:
    """
    Decode a JSON Web Token (JWT) and validate its expiration.

    Args:
        token (str): The JWT to be decoded.

    Returns:
        dict: The decoded payload if valid and not expired.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return (decoded_token
                if decoded_token["expires"] >= time.time() else None)
    except Exception:
        return {}
