from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    password_hash = db.Column(db.String(128))
    
    role = db.Column(db.String(20), default="reader", nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.now)
    
    webhook_url = db.Column(db.String(255), nullable=True)

    loans = db.relationship("Loan", back_populates="user", cascade="all, delete-orphan")

        # setter/getter for password
    @property
    def password(self):
        raise AttributeError("Password not readable")

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "webhook_url": self.webhook_url,
            "registered_at": self.registered_at.isoformat() if self.registered_at else None,
        }
