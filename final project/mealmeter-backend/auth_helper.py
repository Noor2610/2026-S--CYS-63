"""
auth_helper.py
--------------
JWT token creation and verification.
Mirrors the Angular AuthService token logic:
  - token = btoa(user.id + ":" + timestamp)      (frontend, simple)
  - Backend uses proper JWT with HS256 for security
"""

import os
import time
import jwt
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mealmeter-super-secret-jwt-key-2024")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))


def create_token(user_id, role):
    """
    Create a signed JWT token containing user_id and role.
    Expires in JWT_EXPIRY_HOURS hours (default 24).
    """
    payload = {
        "user_id": str(user_id),
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + (JWT_EXPIRY_HOURS * 3600),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    """
    Decode and verify a JWT token.
    Returns the payload dict on success.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload


def _get_token_from_request():
    """
    Extract Bearer token from the Authorization header.
    Returns the token string or None.
    """
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[len("Bearer "):]
    return None


def token_required(f):
    """
    Decorator: protects a route — requires a valid JWT token.
    Injects 'current_user_id' and 'current_user_role' into kwargs.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token_from_request()
        if not token:
            return jsonify({"error": "Authorization token is missing."}), 401
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token. Please log in again."}), 401

        kwargs["current_user_id"] = payload["user_id"]
        kwargs["current_user_role"] = payload["role"]
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """
    Decorator: protects a route — requires a valid JWT token AND admin role.
    Must be used AFTER @token_required (or stacked on top).
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token_from_request()
        if not token:
            return jsonify({"error": "Authorization token is missing."}), 401
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token. Please log in again."}), 401

        if payload.get("role") != "admin":
            return jsonify({"error": "Admin access required."}), 403

        kwargs["current_user_id"] = payload["user_id"]
        kwargs["current_user_role"] = payload["role"]
        return f(*args, **kwargs)

    return decorated
