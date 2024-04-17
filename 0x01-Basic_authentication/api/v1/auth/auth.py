#!/usr/bin/env python3
""" Creating a class for authentication """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Handles authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns true if the path is not in the list of strings
        of excluded paths
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for ex_path in excluded_paths:
            if path.rstrip("/") == ex_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Validating all requests to seure the API """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']
    def current_user(self, request=None) -> TypeVar('user'):
        return None
