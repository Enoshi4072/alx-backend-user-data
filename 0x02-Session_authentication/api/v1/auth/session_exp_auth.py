#!/usr/bin/env python3
""" Class to handle the expiration of a session """
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ To handle session expiration """
    def __init__(self) -> None:
        """ Initializing the class """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0
    
    def create_session(self, user_id=None) :
        """ Creating a session ID"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Returning  a user id from the session dict """
        if session_id is None:
            return None
        session_info = self.user_id_by_session_id.get(session_id)
        if session_info is None:
            return None
        if self.session_duration <= 0:
            return session_info['user_id']
        created_at = session_info.get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session_info['user_id']
