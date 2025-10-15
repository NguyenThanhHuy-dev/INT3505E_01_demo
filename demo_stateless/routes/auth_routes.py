# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.user import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    token = user.generate_token()
    db.session.commit()
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = User.query.filter_by(api_token=token).first()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    user.api_token = None
    db.session.commit()
    return jsonify({"message": "Logged out"}), 200
