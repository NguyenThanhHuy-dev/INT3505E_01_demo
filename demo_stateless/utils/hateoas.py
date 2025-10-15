from flask import url_for

def generate_book_links(book_id=None, cursor=None, next_cursor=None, offset=None, limit=None, page=None, per_page=None):
    links = {
        "list_page": url_for("books_bp.list_books", _external=True),
        "list_offset": url_for("books_bp.list_books_offset", _external=True),
        "list_cursor": url_for("books_bp.list_books_cursor", _external=True),
        "create": url_for("books_bp.create_book", _external=True)
    }

    if cursor is not None:
        links["self"] = url_for("books_bp.list_books_cursor", cursor=cursor, limit=limit, _external=True)
        if next_cursor is not None:
            links["next"] = url_for("books_bp.list_books_cursor", cursor=next_cursor, limit=limit, _external=True)
    if offset is not None:
        links["self"] = url_for("books_bp.list_books_offset", offset=offset, limit=limit, _external=True)
        if limit is not None:
            links["next"] = url_for("books_bp.list_books_offset", offset=offset + limit, limit=limit, _external=True)
            if offset - limit >= 0:
                links["prev"] = url_for("books_bp.list_books_offset", offset=offset - limit, limit=limit, _external=True)
    if page is not None:
        links["self"] = url_for("books_bp.list_books", page=page, per_page=per_page, _external=True)
        if per_page and page is not None:
            links["next"] = url_for("books_bp.list_books", page=page + 1, per_page=per_page, _external=True)
            if page > 1:
                links["prev"] = url_for("books_bp.list_books", page=page - 1, per_page=per_page, _external=True)

    if book_id:
        links.update({
            "self": url_for("books_bp.get_book", book_id=book_id, _external=True),
            "update": url_for("books_bp.update_book", book_id=book_id, _external=True),
            "delete": url_for("books_bp.delete_book", book_id=book_id, _external=True)
        })
    return links


def generate_user_links(user_id=None):
    links = {
        "list": url_for("users_bp.list_users", _external=True),
        "create": url_for("users_bp.create_user", _external=True)
    }
    if user_id:
        links.update({
            "self": url_for("users_bp.get_user", user_id=user_id, _external=True),
            "update": url_for("users_bp.update_user", user_id=user_id, _external=True),
            "delete": url_for("users_bp.delete_user", user_id=user_id, _external=True)
        })
    return links


def generate_loan_links(loan_id=None, user_id=None, book_id=None):
    links = {
        "list": url_for("loans_bp.list_loans", _external=True),
        "create": url_for("loans_bp.create_loan_route", _external=True)
    }
    if loan_id:
        links.update({
            "self": url_for("loans_bp.get_loan_route", loan_id=loan_id, _external=True),
            "return": url_for("loans_bp.return_loan_route", loan_id=loan_id, _external=True)
        })
    if user_id:
        links["user"] = url_for("users_bp.get_user", user_id=user_id, _external=True)
    if book_id:
        links["book"] = url_for("books_bp.get_book", book_id=book_id, _external=True)
    return links
