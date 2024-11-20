from functools import wraps
from flask import request, jsonify, abort
import jwt

JWT_SECRET = "your_secret_key"

def jwt_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            abort(401, description="Token missing")


        try:
            token = token.split()[1]
        except IndexError:
            abort(401, description="Invalid token format")

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            abort(401, description="Token expired")
        except jwt.InvalidTokenError:
            abort(401, description="Invalid token")

        return f(*args, **kwargs)

    return decorated_function
