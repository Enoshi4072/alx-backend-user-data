#!/usr/bin/env python3
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route('/')
def index() -> str:
    """ Return a JSON payload of the form """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """ Implementing the end-point to register a user """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        """ Try to register the user """
        user = AUTH.register_user(email, password)
        """ If successful, return a JSON response """
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        """ If already exists, return a JSON response with a 400 status code """
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
