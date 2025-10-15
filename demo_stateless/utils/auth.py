from functools import wraps
from flask import request, jsonify
from models.user import User

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Authorization token missing"}), 401

        user = User.query.filter_by(api_token=token).first()
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.current_user = user
        return f(*args, **kwargs)
    return decorated
