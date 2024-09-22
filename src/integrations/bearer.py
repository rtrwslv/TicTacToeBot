"""Module for bearer."""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from integrations.auth import decode_jwt


class JWTBearer(HTTPBearer):
    """A class that implements JWT Bearer authentication."""

    def __init__(self, auto_error: bool = True):
        """
        Initialize the JWTBearer instance.

        Args:
            auto_error (bool): If set to True, an HTTPException will be raised.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """
        Call the JWTBearer instance to authenticate a request.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            HTTPAuthorizationCredentials: Credentials extracted from request.

        Raises:
            HTTPException: If the authentication scheme is invalid.
        """
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme. Use Bearer"
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials
        else:
            return HTTPAuthorizationCredentials(scheme="", credentials="")

    def verify_jwt(self, jwtoken: str) -> bool:
        """
        Verify the validity of a JSON Web Token (JWT).

        Args:
            jwtoken (str): The JSON Web Token to be verified.

        Returns:
            bool: True if the token is valid and successfully decoded;
                False if the token is invalid or cannot be decoded.
        """
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except Exception:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
