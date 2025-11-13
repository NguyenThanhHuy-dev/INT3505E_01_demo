from flask import Blueprint, request, jsonify
from api.v2.hateoas import generate_user_links
from services.user_service import (
    create_user_basic,
    get_user_by_id,
    get_all_users,
    update_user_details,
    delete_user_by_id
)
# Lưu ý: @jwt_required() vẫn cần được thêm vào nếu bạn muốn bảo vệ các route này
# Tôi tạm bỏ qua để tập trung vào logic refactor

users_bp = Blueprint("v2_users_bp", __name__)

@users_bp.route("", methods=["POST"], endpoint="create_user")
def create_user():
    data = request.get_json() or {}
    # Logic nghiệp vụ đã được chuyển sang service
    # Service sẽ tự raise lỗi 400, 409 nếu có
    user = create_user_basic(data) 
    
    return jsonify({
        "message": "User created",
        "user": user.to_dict(),
        "_links": generate_user_links(user.id)
    }), 201

@users_bp.route("/<int:user_id>", methods=["GET"], endpoint="get_user")
def get_user(user_id):
    # Service sẽ tự raise lỗi 404 nếu không tìm thấy
    user = get_user_by_id(user_id) 
    
    borrowed = [loan.to_dict() for loan in user.loans]
    return jsonify({
        "user": user.to_dict(),
        "loans": borrowed,
        "_links": generate_user_links(user.id)
    }), 200

@users_bp.route("", methods=["GET"], endpoint="list_users")
def list_users():
    users = get_all_users()
    return jsonify({
        "users": [u.to_dict() for u in users],
        "_links": generate_user_links()
    }), 200

@users_bp.route("/<int:user_id>", methods=["PUT"], endpoint="update_user")
def update_user(user_id):
    data = request.get_json() or {}
    
    # Service sẽ tự raise lỗi 404, 409 nếu có
    user = update_user_details(user_id, data) 
    
    return jsonify({
        "message": "User updated",
        "user": user.to_dict(),
        "_links": generate_user_links(user.id)
    }), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"], endpoint="delete_user")
def delete_user(user_id):
    # Service sẽ tự raise lỗi 404, 409 nếu có
    delete_user_by_id(user_id) 
    
    return jsonify({
        "message": "User deleted",
        "_links": generate_user_links()
    }), 200