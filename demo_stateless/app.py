# app.py
import time
import logging
import os
from flask import Flask, send_from_directory, request, jsonify
from config import Config
from database import db, migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# --- Import cho Logging, Monitoring & Rate Limit ---
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# --- Import Blueprints cũ của bạn ---
from api.v2.auth_routes import auth_bp
from api.v2.book_routes import books_bp
from api.v2.user_routes import users_bp
from api.v2.loan_routes import loans_bp
from api.v1.book_routes import books_v1_bp
from api.v1.user_routes import users_v1_bp
from api.v1.loan_routes import loans_v1_bp
from utils.errors import register_error_handlers
from utils.token_blocklist import jwt_blacklist

# 1. CẤU HÌNH LOGGING (Thay thế Winston)
# Tạo logger xuất ra định dạng JSON để hệ thống monitoring dễ đọc
logger = logging.getLogger("library_api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(message)s %(method)s %(path)s %(ip)s %(status)s %(duration)s'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# 2. CẤU HÌNH RATE LIMITER
# Mặc định: 200 request/ngày và 50 request/giờ cho mỗi IP
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# 3. CẤU HÌNH PROMETHEUS METRICS
# Đếm tổng số request
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
# Đo thời gian phản hồi (Latency)
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['endpoint'])


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["JWT_SECRET_KEY"] = "super-secret-key" # Lưu ý: Nên để trong biến môi trường

    # --- Init các Extension ---
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    limiter.init_app(app)  # Kích hoạt Rate Limiter

    # --- Middleware cho Monitoring & Logging ---
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def record_metrics_and_log(response):
        # Tính thời gian xử lý
        if hasattr(request, 'start_time'):
            resp_time = time.time() - request.start_time
        else:
            resp_time = 0

        # Ghi Metrics cho Prometheus
        # Dùng request.url_rule để group các url giống nhau (ví dụ /users/<id>)
        endpoint = str(request.url_rule) if request.url_rule else "not_found"
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(resp_time)
        REQUEST_COUNT.labels(
            method=request.method, 
            endpoint=endpoint, 
            status=response.status_code
        ).inc()

        # Ghi Audit Log (JSON)
        logger.info("Request processed", extra={
            'method': request.method,
            'path': request.path,
            'ip': request.remote_addr,
            'status': response.status_code,
            'duration': round(resp_time, 4)
        })
        
        return response

    # --- JWT Blocklist Check ---
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in jwt_blacklist

    # --- Register Blueprints ---
    app.register_blueprint(books_v1_bp, url_prefix='/api/v1/books')
    app.register_blueprint(users_v1_bp, url_prefix='/api/v1/users')
    app.register_blueprint(loans_v1_bp, url_prefix='/api/v1/loans')
    
    app.register_blueprint(auth_bp, url_prefix="/api/v2/auth")
    app.register_blueprint(books_bp, url_prefix='/api/v2/books')
    app.register_blueprint(users_bp, url_prefix='/api/v2/users')
    app.register_blueprint(loans_bp, url_prefix='/api/v2/loans')

    register_error_handlers(app)

    # --- Swagger UI setup ---
    SWAGGER_URL = '/api/v2/docs'
    API_URL = '/api/openapi.yaml'
    
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL,
        config={'app_name': "Library Management API v2"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/api/openapi.yaml")
    def openapi_yaml():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(current_dir, "openapi.yaml", mimetype="text/yaml")

    # --- Endpoint Metrics cho Prometheus ---
    @app.route('/metrics')
    def metrics():
        # Endpoint này để Prometheus server chọc vào lấy dữ liệu
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

    @app.route("/")
    def index():
        return {"message": "Library API (Flask) - Running with Observability"}, 200
    
    # --- Endpoint Test Rate Limit ---
    @app.route("/api/spam-me")
    @limiter.limit("3 per minute") # Chỉ cho phép 3 lần/phút
    def spam_test():
        return {"message": "You haven't been blocked yet!"}

    # Xử lý lỗi khi bị Rate Limit chặn
    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning("Rate limit exceeded", extra={'ip': request.remote_addr})
        return jsonify({"error": "Too Many Requests", "description": str(e.description)}), 429

    app.jwt_blacklist = jwt_blacklist
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)