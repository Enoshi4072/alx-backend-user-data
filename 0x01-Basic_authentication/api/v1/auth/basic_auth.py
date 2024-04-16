#!/usr/bin/env python3
""" Class to handle basic authentication """
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Handling basic auth
    - Returns Base64 part of the Authorization header for basic auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Returns a decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64
        decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
       """
       Returns the user instance based on his email and password
       """
       if user_email is None or not isinstance(user_email, str):
           return None
       if user_pwd is None or not isinstance(user_pwd, str):
           return None
       users = User.search({'email': user_email})
       if not users:
           return None
       user = users[0]
       if not user.is_valid_password(user_pwd):
           return None
       return user
    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request """
        if request is None:
            return None
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        if base64_authorization_header is None:
            return None
        decoded_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        if decoded_authorization_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_authorization_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
