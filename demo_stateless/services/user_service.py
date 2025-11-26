from database import db
from models.user import User
from utils.errors import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)


def register_user(data):
    """
    Xử lý logic đăng ký người dùng (từ auth_routes).
    """
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        raise BadRequestError("Tên, email, và mật khẩu là bắt buộc")

    if User.query.filter_by(email=email).first():
        raise ConflictError("Email này đã được đăng ký")

    user = User(name=name, email=email)
    user.password = password  # Setter trong Model sẽ tự động hash

    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(data):
    """
    Xử lý logic đăng nhập người dùng (từ auth_routes).
    """
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise BadRequestError("Email và mật khẩu là bắt buộc")

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        raise UnauthorizedError("Email hoặc mật khẩu không hợp lệ")

    return user


def get_user_by_id(user_id):
    """
    Lấy thông tin một người dùng (từ user_routes và auth_routes).
    """
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Không tìm thấy người dùng")
    return user


def get_all_users():
    """
    Lấy danh sách tất cả người dùng (từ user_routes).
    """
    return User.query.all()


def create_user_basic(data):
    """
    Xử lý logic tạo user cơ bản (từ user_routes).
    LƯU Ý: Route này không set password, có thể bạn muốn
    loại bỏ route này và chỉ dùng /auth/register.
    """
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        raise BadRequestError("Tên và email là bắt buộc")

    if User.query.filter_by(email=email).first():
        raise ConflictError("Email này đã được đăng ký")

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def update_user_details(user_id, data):
    """
    Xử lý logic cập nhật người dùng (từ user_routes).
    """
    user = get_user_by_id(user_id)  # Tái sử dụng hàm get_user_by_id

    if "name" in data:
        user.name = data["name"]

    if "email" in data:
        new_email = data["email"]
        existing = User.query.filter_by(email=new_email).first()
        if existing and existing.id != user_id:
            raise ConflictError("Email này đã được sử dụng")
        user.email = new_email

    db.session.commit()
    return user


def delete_user_by_id(user_id):
    """
    Xử lý logic xóa người dùng (từ user_routes).
    """
    user = get_user_by_id(user_id)  # Tái sử dụng hàm get_user_by_id

    if user.loans:
        raise ConflictError("Không thể xóa người dùng đang có sách mượn")

    db.session.delete(user)
    db.session.commit()
    return True
