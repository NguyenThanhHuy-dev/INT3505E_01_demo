from database import db
from datetime import datetime, timedelta
from utils.hateoas import generate_loan_links

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    status = db.Column(db.String(20), default="borrowed", nullable=False)  # borrowed, returned, overdue
    borrowed_at = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="loans")
    book = db.relationship("Book", back_populates="loans")

    def set_due_default(self, days=14):
        if not self.borrowed_at:
            self.borrowed_at = datetime.now()
        self.due_date = self.borrowed_at + timedelta(days=days)

    def is_overdue(self):
        if self.status == "borrowed" and self.due_date:
            return datetime.now() > self.due_date
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "status": self.status,
            "borrowed_at": self.borrowed_at.isoformat() if self.borrowed_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "returned_at": self.returned_at.isoformat() if self.returned_at else None,
        }
