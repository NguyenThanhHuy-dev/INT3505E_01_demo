from database import db
from models.loan import Loan
from models.user import User
from models.book import Book
from datetime import datetime, timedelta

def borrow_book(user_id, book_id, days=14):
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    if not user or not book:
        return {"error": "User or Book not found"}
    if book.copies_available <= 0:
        return {"error": "No copies available"}
    loan = Loan(user_id=user.id, book_id=book.id)
    loan.set_due_default(days)
    book.copies_available -= 1
    db.session.add(loan)
    db.session.commit()
    return loan

def return_book(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return {"error": "Loan not found"}
    if loan.status == "returned":
        return {"error": "Already returned"}

    loan.returned_at = datetime.utcnow()
    loan.status = "overdue" if loan.is_overdue() else "returned"

    book = Book.query.get(loan.book_id)
    if book:
        book.copies_available = min(book.copies_total, book.copies_available + 1)

    db.session.commit()
    return loan


def get_loan(loan_id):
    return Loan.query.get(loan_id)
