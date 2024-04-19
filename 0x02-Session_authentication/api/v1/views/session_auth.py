#!/usr/bin/env python3
"""
Handling all routes for session auth
"""
from models.user import User
from api.v1.views import app_views

import os
from typing import Tuple
from flask import abort, jsonify, request

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    Handling login requests
    Return:
        - JSON representation of a User object
    """
    er_msg = {'error': 'no user found for this email'}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if len(users) <= 0:
        return jsonify(er_msg), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        response = jsonify(users[0].to_json())
        response.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return response
    return jsonify({'error': 'wrong password'}), 401

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """ Logging out a user"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
