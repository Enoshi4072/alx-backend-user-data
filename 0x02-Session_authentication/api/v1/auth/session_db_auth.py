#!/usr/bin/env python3
""" Handling session auth from the db """
from .session_exp_auth import SessionExpAuth
from  uuid import uuid4
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Creating a session in the db """
    
    def create_session(self, user_id=None):
        """ Creating a session """
        session_id = str(uuid4())
        new_session = UserSession(user_id=user_id, session_id=session_id)
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': new_session.created_at
                }
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returning the User ID associated with a session ID """
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

    def destroy_session(self, request=None):
        """ Destroying the user session based on the session ID from the request cookie """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session[0].delete()
        del self.user_id_by_session_id[session_id]
        return True
