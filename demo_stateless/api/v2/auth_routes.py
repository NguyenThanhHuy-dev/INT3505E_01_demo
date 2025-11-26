from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from utils.token_blocklist import jwt_blacklist
from services.user_service import (
    register_user, 
    authenticate_user, 
    get_user_by_id
)

auth_bp = Blueprint("v2_auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    
    # Service sẽ tự raise lỗi 400, 409
    user = register_user(data) 

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    
    # Service sẽ tự raise lỗi 400, 401
    user = authenticate_user(data) 

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


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = int(get_jwt_identity())
    
    # Tái sử dụng service, tự raise 404
    user = get_user_by_id(current_user_id) 
    
    return jsonify(user.to_dict()), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)
    token_type = get_jwt()["type"]
    return jsonify({
        "message": f"{token_type.capitalize()} token revoked successfully"
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(minutes=1)
    )
    return jsonify({
        "access_token": new_access_token
    }), 200