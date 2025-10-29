# loan_routes.py
from flask import Blueprint, request, jsonify
from api.v1.hateoas import generate_loan_links
from services.loan_service import (
    borrow_book as borrow_book_service,
    return_book as return_book_service,
    get_loan as get_loan_service
)
from models.loan import Loan

loans_v1_bp = Blueprint("v1_loans_bp", __name__)

@loans_v1_bp.route("", methods=["POST"], endpoint="create_loan")
def create_loan():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    days = data.get("days", 14)

    loan = borrow_book_service(user_id, book_id, days)
    if isinstance(loan, dict) and "error" in loan:
        return jsonify(loan), 400

    return jsonify({
        "message": "Borrowed successfully",
        "loan": loan.to_dict(),
        "_links": generate_loan_links(loan.id, user_id=loan.user_id, book_id=loan.book_id)
    }), 201


@loans_v1_bp.route("/<int:loan_id>/return", methods=["PUT"], endpoint="return_loan")
def return_loan(loan_id):
    res = return_book_service(loan_id)
    if isinstance(res, dict) and "error" in res:
        return jsonify(res), 400
    return jsonify({
        "message": "Returned successfully",
        "loan": res.to_dict(),
        "_links": generate_loan_links(res.id, user_id=res.user_id, book_id=res.book_id)
    }), 200


@loans_v1_bp.route("/<int:loan_id>", methods=["GET"], endpoint="get_loan")
def get_loan(loan_id):
    loan = get_loan_service(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    return jsonify({
        "loan": loan.to_dict(),
        "_links": generate_loan_links(loan.id, user_id=loan.user_id, book_id=loan.book_id)
    }), 200


@loans_v1_bp.route("", methods=["GET"], endpoint="list_loans")
def list_loans():
    loans = Loan.query.all()
    return jsonify({
        "loans": [loan.to_dict() for loan in loans],
        "_links": generate_loan_links()
    }), 200
