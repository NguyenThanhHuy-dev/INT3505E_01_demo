from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from models.user import User
from database import db
from flask_jwt_extended import jwt_required, get_jwt
from utils.token_blocklist import jwt_blacklist

auth_bp = Blueprint("v2_auth_bp", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Missing fields"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(name=name, email=email)
    user.password = password  # simple example — should hash later
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid credentials"}), 401


    # token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=1))
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=1)
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=30)
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200


# PROFILE (protected)
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(verify_type=False)  # chấp nhận cả access và refresh
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)
    token_type = get_jwt()["type"]
    return jsonify({
        "message": f"{token_type.capitalize()} token revoked successfully"
    }), 200



@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # 👈 chỉ cho phép refresh token
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(minutes=1)
    )
    return jsonify({
        "access_token": new_access_token
    }), 200