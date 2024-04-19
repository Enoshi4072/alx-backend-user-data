#!/usr/bin/env python3
""" Handling session authentication """
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Class to handle session Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        To create a session ID for each session
        - Return: session_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user = self.user_id_by_session_id.get(session_id)
        return user

    def current_user(self, request=None):
        """ Returns a user instance based on a cookie value """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ A method that deletes the user session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
