#!/usr/bin/env python3
""" A module for Encription using bcrypt """
import bcrypt
import typing


def hash_password(password: str) -> bytes:
    """ Hashes a password using bcrypt """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str):
    """ Check is plaintext password matches a hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
