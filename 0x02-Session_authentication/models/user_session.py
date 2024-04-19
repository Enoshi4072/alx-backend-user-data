#!/usr/bin/env python3
""" Handling session autj system located in the database """
from .base import Base
from sqlalchemy import String, Column


class UserSession(Base):
    """ Implementing session auth in the db """
    __tablename__ = 'user_sessions'
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """ Initialize the session """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
