from flask import Blueprint, request, jsonify
from api.v2.hateoas import generate_loan_links
from services.loan_service import (
    borrow_book as borrow_book_service,
    return_book as return_book_service,
    get_loan as get_loan_service,
    get_all_loans as get_all_loans_service  # <-- THÊM MỚI
)
from flask_jwt_extended import jwt_required

loans_bp = Blueprint("v2_loans_bp", __name__)

@loans_bp.route("", methods=["POST"], endpoint="create_loan")
@jwt_required()
def create_loan():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    days = data.get("days", 14)

    # Chỉ cần gọi service, service sẽ tự raise lỗi
    loan = borrow_book_service(user_id, book_id, days)

    # BỎ: Khối `if isinstance(loan, dict) and "error" in loan:`
    # vì nó là code "chết" (dead code).

    return jsonify({
        "message": "Borrowed successfully",
        "loan": loan.to_dict(),
        "_links": generate_loan_links(loan.id, user_id=loan.user_id, book_id=loan.book_id)
    }), 201


@loans_bp.route("/<int:loan_id>/return", methods=["PUT"], endpoint="return_loan")
@jwt_required()
def return_loan(loan_id):
    # Chỉ cần gọi service, service sẽ tự raise lỗi
    loan = return_book_service(loan_id)
    
    # BỎ: Khối `if isinstance(res, dict) and "error" in res:`
    # vì nó là code "chết".

    return jsonify({
        "message": "Returned successfully",
        "loan": loan.to_dict(),
        "_links": generate_loan_links(loan.id, user_id=loan.user_id, book_id=loan.book_id)
    }), 200


@loans_bp.route("/<int:loan_id>", methods=["GET"], endpoint="get_loan")
@jwt_required()
def get_loan(loan_id):
    # Service sẽ tự raise NotFoundError
    loan = get_loan_service(loan_id)
    
    # BỎ: Khối `if not loan:` vì nó là code thừa.
    
    return jsonify({
        "loan": loan.to_dict(),
        "_links": generate_loan_links(loan.id, user_id=loan.user_id, book_id=loan.book_id)
    }), 200


@loans_bp.route("", methods=["GET"], endpoint="list_loans")
@jwt_required()
def list_loans():
    # SỬA: Gọi service thay vì query trực tiếp
    loans = get_all_loans_service()
    
    return jsonify({
        "loans": [loan.to_dict() for loan in loans],
        "_links": generate_loan_links()
    }), 200