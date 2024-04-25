#!/usr/bin/env python3
""" Takes in a password string arguments and returns bytes """
import bcrypt
def _hash_password(password: str) -> bytes:
    #Generate a salted hash of the input passowrd using bcrypt.hashpw
    #Generate a salt
    salt = bcrypt.gensalt()
    #hash the password to the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    #return the hashed password as bytes
    return hashed_password
