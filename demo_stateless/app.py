# app.py
from flask import Flask
from config import Config
from database import db, migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
from api.v1.book_routes import books_bp
from api.v1.user_routes import users_bp
from api.v1.loan_routes import loans_bp

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    app.register_blueprint(books_bp, url_prefix='/api/v1/books')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(loans_bp, url_prefix='/api/v1/loans')

    from utils.errors import register_error_handlers
    register_error_handlers(app)

    @app.route("/")
    def index():
        return {"message": "Library API (Flask) - running"}, 200


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)