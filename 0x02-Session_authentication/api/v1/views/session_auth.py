from flask import jsonify, request
from models.user import User
from api.v1.views import app_views
from api.v1.app import auth
from typing import Tuple
@app_views.route('/auth_session/login', methods=['POST', 'GET'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handles user login using Session authentication."""
    if request.method == 'POST':
        # Retrieve email and password parameters from form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email is missing or empty
        if not email:
            return jsonify({'error': 'email missing'}), 400

        # Check if password is missing or empty
        if not password:
            return jsonify({'error': 'password missing'}), 400

        # Retrieve User instance based on the email
        user = User.search({'email': email})

        # If no User found, return error
        if not user:
            return jsonify({'error': 'no user found for this email'}), 404

        # Check if the provided password is correct
        if not user.is_valid_password(password):
            return jsonify({'error': 'wrong password'}), 401

        # Create a Session ID for the User ID
        session_id = auth.create_session(user.id)

        # Return the dictionary representation of the User
        user_json = user.to_json()

        # Set the cookie to the response
        response = jsonify(user_json)
        response.set_cookie(auth.session_cookie_name, session_id)

        return response, 200
    else:
        # If method is not allowed, return error
        return jsonify({'error': 'Method Not Allowed'}), 40i5
