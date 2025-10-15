from database import db
from datetime import datetime
from utils.hateoas import generate_book_links

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(32), unique=True, nullable=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    copies_total = db.Column(db.Integer, default=1, nullable=False)
    copies_available = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    loans = db.relationship("Loan", back_populates="book", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "copies_total": self.copies_total,
            "copies_available": self.copies_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }