# app.py
from flask import Flask, send_from_directory
from config import Config
from database import db, migrate
from flask_jwt_extended import JWTManager
from api.v2.auth_routes import auth_bp
from api.v2.book_routes import books_bp
from api.v2.user_routes import users_bp
from api.v2.loan_routes import loans_bp
from utils.errors import register_error_handlers
from utils.token_blocklist import jwt_blacklist
from flask_swagger_ui import get_swaggerui_blueprint
import os

from api.v1.book_routes import books_v1_bp
from api.v1.user_routes import users_v1_bp
from api.v1.loan_routes import loans_v1_bp

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    
    # --- Database & JWT setup ---
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in jwt_blacklist

    # --- Register blueprints ---
    app.register_blueprint(books_v1_bp, url_prefix='/api/v1/books')
    app.register_blueprint(users_v1_bp, url_prefix='/api/v1/users')
    app.register_blueprint(loans_v1_bp, url_prefix='/api/v1/loans')
    
    app.register_blueprint(auth_bp, url_prefix="/api/v2/auth")
    app.register_blueprint(books_bp, url_prefix='/api/v2/books')
    app.register_blueprint(users_bp, url_prefix='/api/v2/users')
    app.register_blueprint(loans_bp, url_prefix='/api/v2/loans')

    register_error_handlers(app)

    # --- Swagger UI setup ---
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/openapi.yaml'
    
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Library Management API v2"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Serve the OpenAPI YAML file
    @app.route("/api/openapi.yaml")
    def openapi_yaml():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(current_dir, "openapi.yaml", mimetype="text/yaml")

    @app.route("/")
    def index():
        return {"message": "Library API (Flask) - running"}, 200

    app.jwt_blacklist = jwt_blacklist
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
