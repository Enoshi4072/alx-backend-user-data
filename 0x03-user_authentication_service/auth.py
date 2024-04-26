#!/usr/bin/env python3
""" Takes in a password string arguments and returns bytes """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """ Generate a salted hash of the input passowrd using bcrypt.hashpw """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """ Returns a string rep of a new UUID module """
    return str(uuid.uuid4())


class Auth:
    """ Auth class to interact with the auth database """
    def __init__(self):
        """ Doing the initialisation """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registering users """
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            """ Hashing the password """
            hashed_password = _hash_password(password)
            """ Adding a new user to the db """
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Try locating by email """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                return bcrypt.checkpw(
                        password.encode('utf-8'),
                        existing_user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """ Takes an email string arg and returns the session ID """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id
                self._db._session.commit()
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Gets a user based on the session id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Takes a single user_id integer argument and returns None """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generating a reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        user.reset_token = reset_token
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Handling the user's reset password option """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            h_password = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=h_password,
                    reset_token=None)
        except NoResultFound:
            raise ValueError()
