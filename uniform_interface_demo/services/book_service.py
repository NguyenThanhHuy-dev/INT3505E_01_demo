from database import db
from models.book import Book
from sqlalchemy import and_

def create_book(data):
    try:
        book = Book(
            isbn=data.get("isbn"),
            title=data.get("title", "Untitled"),
            author=data.get("author", "Unknown"),
            year=data.get("year"),
            genre=data.get("genre"),
            copies_total=int(data.get("copies_total", 1)),
            copies_available=int(data.get("copies_total", 1))
        )
        db.session.add(book)
        db.session.commit()
        return book
    except Exception as e:
        db.session.rollback()
        raise e


def get_books_paginated(filters, page=1, per_page=10):
    q = Book.query
    if filters.get("author"):
        q = q.filter(Book.author.ilike(f"%{filters['author']}%"))
    if filters.get("genre"):
        q = q.filter(Book.genre.ilike(f"%{filters['genre']}%"))
    if filters.get("available") in ("true", "True", "1", True):
        q = q.filter(Book.copies_available > 0)
    pagination = q.order_by(Book.id).paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages

def get_book(book_id):
    return Book.query.get(book_id)

def update_book(book_id, data):
    book = Book.query.get(book_id)
    if not book:
        return None
    for k in ("isbn", "title", "author", "year", "genre", "copies_total"):
        if k in data:
            setattr(book, k, data[k])
    # ensure copies_available <= copies_total
    if "copies_total" in data:
        new_total = int(data["copies_total"])
        if book.copies_available > new_total:
            book.copies_available = new_total
    db.session.commit()
    return book

def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return False
    db.session.delete(book)
    db.session.commit()
    return True
