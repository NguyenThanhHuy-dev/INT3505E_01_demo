# app.py
from flask import Flask
from config import Config
from database import db, migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
from api.v2.auth_routes import auth_bp
from api.v2.book_routes import books_bp
from api.v2.user_routes import users_bp
from api.v2.loan_routes import loans_bp
from utils.errors import register_error_handlers
from utils.token_blocklist import jwt_blacklist

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]  # "JWT ID" — định danh duy nhất của token
        return jti in jwt_blacklist
    
    app.register_blueprint(auth_bp, url_prefix="/api/v2/auth")
    app.register_blueprint(books_bp, url_prefix='/api/v2/books')
    app.register_blueprint(users_bp, url_prefix='/api/v2/users')
    app.register_blueprint(loans_bp, url_prefix='/api/v2/loans')

    register_error_handlers(app)

    @app.route("/")
    def index():
        return {"message": "Library API (Flask) - running"}, 200

    app.jwt_blacklist = jwt_blacklist

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)