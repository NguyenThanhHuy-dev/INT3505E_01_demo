import secrets
from database import db
from datetime import datetime
from utils.hateoas import generate_user_links

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default="reader", nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.now)

    api_token = db.Column(db.String(64), unique=True, nullable=True)  # NEW FIELD

    loans = db.relationship("Loan", back_populates="user", cascade="all, delete-orphan")

    def generate_token(self):
        self.api_token = secrets.token_hex(32)
        return self.api_token

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "registered_at": self.registered_at.isoformat() if self.registered_at else None,
        }
