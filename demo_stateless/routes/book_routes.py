from flask import Blueprint, make_response, request, jsonify, url_for
from services.book_service import create_book, get_books_paginated, get_book, update_book, delete_book, get_books_offset, get_books_cursor
from utils.cache import generate_etag
from utils.hateoas import generate_book_links

books_bp = Blueprint("books_bp", __name__)

@books_bp.route("", methods=["GET"], endpoint="list_books")
def list_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    filters = {
        "author": request.args.get("author"),
        "genre": request.args.get("genre"),
        "available": request.args.get("available")
    }
    items, total, pages = get_books_paginated(filters, page, per_page)
    payload = {
        "books": [b.to_dict() for b in items],
        "meta": {"page": page, "per_page": per_page, "total": total, "pages": pages},
        "_links": generate_book_links(page=page, per_page=per_page)
    }
    return jsonify(payload), 200


@books_bp.route("", methods=["POST"], endpoint="create_book")
def create_book_route():
    data = request.get_json() or {}
    book = create_book(data)
    resp = {
        "message": "Book created",
        "book": book.to_dict(),
        "_links": generate_book_links(book.id)
    }
    return jsonify(resp), 201


@books_bp.route("/<int:book_id>", methods=["GET"], endpoint="get_book")
def get_book_route(book_id):
    book = get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    
    book_data = book.to_dict()
    etag = generate_etag(book_data)
    
    if request.headers.get("If-None-Match") == etag:
        return '', 304  # Not Modified
    
    resp = make_response(jsonify({ 
        "book": book_data,
        "_links": generate_book_links(book.id),
    }))
    

    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "public, max-age=60"
    
    return resp, 200

@books_bp.route("/offset", methods=["GET"], endpoint="list_books_offset")
def list_books_offset():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))
    filters = {
        "author": request.args.get("author"),
        "genre": request.args.get("genre"),
        "available": request.args.get("available")
    }
    items, total = get_books_offset(filters, offset, limit)
    payload = {
        "books": [b.to_dict() for b in items],
        "meta": {"offset": offset, "limit": limit, "total": total},
        "_links": generate_book_links(offset=offset, limit=limit)
    }
    return jsonify(payload), 200

@books_bp.route("/cursor", methods=["GET"], endpoint="list_books_cursor")
def list_books_cursor():
    cursor = request.args.get("cursor", None, type=int)
    limit = int(request.args.get("limit", 10))
    filters = {
        "author": request.args.get("author"),
        "genre": request.args.get("genre"),
        "available": request.args.get("available")
    }
    items, next_cursor = get_books_cursor(filters, cursor, limit)
    payload = {
        "books": [b.to_dict() for b in items],
        "meta": {"cursor": cursor, "limit": limit, "next_cursor": next_cursor},
        "_links": generate_book_links(cursor=cursor, next_cursor=next_cursor, limit=limit)
    }
    return jsonify(payload), 200


@books_bp.route("/<int:book_id>", methods=["PUT"], endpoint="update_book")
def update_book_route(book_id):
    data = request.get_json() or {}
    book = update_book(book_id, data)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({
        "message": "Book updated",
        "book": book.to_dict(),
        "_links": generate_book_links(book.id)
    }), 200


@books_bp.route("/<int:book_id>", methods=["DELETE"], endpoint="delete_book")
def delete_book_route(book_id):
    ok = delete_book(book_id)
    if not ok:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({
        "message": "Book deleted",
        "_links": generate_book_links()
    }), 200
