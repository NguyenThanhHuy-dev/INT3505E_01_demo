# demo_stateless/api/v2/hateoas.py
from flask import url_for

BASE = "v2"  # đảm bảo đồng bộ prefix blueprint

def generate_book_links(book_id=None, cursor=None, next_cursor=None, offset=None, limit=None, page=None, per_page=None):
    links = {}

    # Các link chung
    try:
        links["list_page"] = url_for(f"{BASE}_books_bp.list_books", _external=True)
    except:
        pass

    try:
        links["list_offset"] = url_for(f"{BASE}_books_bp.list_books_offset", _external=True)
    except:
        pass

    try:
        links["list_cursor"] = url_for(f"{BASE}_books_bp.list_books_cursor", _external=True)
    except:
        pass

    try:
        links["create"] = url_for(f"{BASE}_books_bp.create_book", _external=True)
    except:
        pass

    # Xử lý cursor-based pagination
    if cursor is not None:
        try:
            links["self"] = url_for(f"{BASE}_books_bp.list_books_cursor", cursor=cursor, limit=limit, _external=True)
            if next_cursor is not None:
                links["next"] = url_for(f"{BASE}_books_bp.list_books_cursor", cursor=next_cursor, limit=limit, _external=True)
        except:
            pass

    # Xử lý offset-based pagination
    if offset is not None:
        try:
            links["self_offset"] = url_for(f"{BASE}_books_bp.list_books_offset", offset=offset, limit=limit, _external=True)
            if limit is not None:
                links["next_offset"] = url_for(f"{BASE}_books_bp.list_books_offset", offset=offset + limit, limit=limit, _external=True)
                if offset - limit >= 0:
                    links["prev_offset"] = url_for(f"{BASE}_books_bp.list_books_offset", offset=offset - limit, limit=limit, _external=True)
        except:
            pass

    # Xử lý page-based pagination
    if page is not None:
        try:
            links["self_page"] = url_for(f"{BASE}_books_bp.list_books", page=page, per_page=per_page, _external=True)
            if per_page and page is not None:
                links["next_page"] = url_for(f"{BASE}_books_bp.list_books", page=page + 1, per_page=per_page, _external=True)
                if page > 1:
                    links["prev_page"] = url_for(f"{BASE}_books_bp.list_books", page=page - 1, per_page=per_page, _external=True)
        except:
            pass

    # Nếu có book_id → thêm các thao tác chi tiết
    if book_id:
        try:
            links.update({
                "self": url_for(f"{BASE}_books_bp.get_book", book_id=book_id, _external=True),
                "update": url_for(f"{BASE}_books_bp.update_book", book_id=book_id, _external=True),
                "delete": url_for(f"{BASE}_books_bp.delete_book", book_id=book_id, _external=True)
            })
        except:
            pass

    return links


def generate_user_links(user_id=None):
    links = {}

    try:
        links["list"] = url_for(f"{BASE}_users_bp.list_users", _external=True)
        links["create"] = url_for(f"{BASE}_users_bp.create_user", _external=True)
    except:
        pass

    if user_id:
        try:
            links.update({
                "self": url_for(f"{BASE}_users_bp.get_user", user_id=user_id, _external=True),
                "update": url_for(f"{BASE}_users_bp.update_user", user_id=user_id, _external=True),
                "delete": url_for(f"{BASE}_users_bp.delete_user", user_id=user_id, _external=True)
            })
        except:
            pass

    return links


def generate_loan_links(loan_id=None, user_id=None, book_id=None):
    links = {}

    try:
        links["list"] = url_for(f"{BASE}_loans_bp.list_loans", _external=True)
        links["create"] = url_for(f"{BASE}_loans_bp.create_loan", _external=True)
    except:
        pass

    if loan_id:
        try:
            links.update({
                "self": url_for(f"{BASE}_loans_bp.get_loan", loan_id=loan_id, _external=True),
                "return": url_for(f"{BASE}_loans_bp.return_loan", loan_id=loan_id, _external=True)
            })
        except:
            pass

    if user_id:
        try:
            links["user"] = url_for(f"{BASE}_users_bp.get_user", user_id=user_id, _external=True)
        except:
            pass

    if book_id:
        try:
            links["book"] = url_for(f"{BASE}_books_bp.get_book", book_id=book_id, _external=True)
        except:
            pass

    return links
