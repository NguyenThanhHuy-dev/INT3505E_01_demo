from flask import Flask, jsonify, request, url_for
from config import Config
from database import db, migrate
from models.book import Book
from models.user import User
from models.loan import Loan
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    from routes.book_routes import books_bp
    from routes.user_routes import users_bp
    from routes.loan_routes import loans_bp

    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(loans_bp, url_prefix='/loans')

    from utils.errors import register_error_handlers
    register_error_handlers(app)

    @app.route("/")
    def index():
        return {"message": "Library API (Flask) - running"}, 200


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)