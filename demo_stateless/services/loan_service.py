from database import db
from models.loan import Loan
from models.user import User
from models.book import Book
from datetime import datetime, timedelta

import requests
import logging

from utils.errors import ConflictError, NotFoundError

logger = logging.getLogger(__name__)


def send_notification_webhook(user, event_type, data):
    if not user.webhook_url:
        return  # User không đăng ký webhook thì bỏ qua

    payload = {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "user_email": user.email,
        "data": data,
    }

    try:
        # Gửi POST request tới URL của user, timeout để tránh treo server
        response = requests.post(user.webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(f"Webhook sent to {user.email} for event {event_type}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send webhook to {user.email}: {e}")


def borrow_book(user_id, book_id, days=14):
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    if not user or not book:
        raise NotFoundError("User or Book not found")
    if book.copies_available <= 0:
        raise ConflictError("No copies available")
    loan = Loan(user_id=user.id, book_id=book.id)
    loan.set_due_default(days)
    book.copies_available -= 1
    db.session.add(loan)
    db.session.commit()

    send_notification_webhook(
        user,
        "BOOK_BORROWED",
        {
            "book_title": book.title,
            "loan_id": loan.id,
            "due_date": loan.due_date.isoformat() if loan.due_date else None,
        },
    )

    return loan


def return_book(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        raise NotFoundError("Loan not found")
    if loan.status == "returned":
        raise ConflictError("Already returned")

    loan.returned_at = datetime.utcnow()
    loan.status = "overdue" if loan.is_overdue() else "returned"

    book = Book.query.get(loan.book_id)
    if book:
        book.copies_available = min(book.copies_total, book.copies_available + 1)

    db.session.commit()

    user = User.query.get(loan.user_id)

    if user:
        send_notification_webhook(
            user,
            "BOOK_RETURNED",
            {
                "book_id": loan.book_id,
                "loan_id": loan.id,
                "returned_at": loan.returned_at.isoformat(),
            },
        )

    return loan


def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        raise NotFoundError("Loan not found")
    return loan


def get_all_loans():
    # Lấy danh sách tất cả các lượt mượn."
    return Loan.query.all()
