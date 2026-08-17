import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import os
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "trustbank_default_secret_key_2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
# =============================== Tạo hashed Password ===============================


def hashed_password_sv(password: str) -> str:

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password.decode("utf-8")


# =============================== TẠO ACCESS TOKEN ===============================
def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire_time})

    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return token


# =============================== VERIFY PASSWORD ===============================
def verify_password(password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(password.encode("utf-8"),
                          hashed_password.encode("utf-8"))


# =============================== REGION ===============================
def register_user_sv(user_inp: UserRegisterRequest, db: Session):

    exists_username = db.query(UserModel).filter(
        UserModel.username == user_inp.username).first()

    if exists_username:
        return "EXISTS_USERNAME"

    # hashed password
    hashed_pwd = hashed_password_sv(user_inp.password)

    # ổn thì tạo
    user_dict = user_inp.model_dump(exclude={"password"})

    user_data = UserModel(**user_dict,
                          hashed_password=hashed_pwd)

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return user_data

# =============================== END REGION ===============================


# =============================== REGION ===============================
def user_login_sv(login_inp: UserLoginRequest, db: Session):

    user = db.query(UserModel).filter(
        UserModel.username == login_inp.username).first()

    if not user:
        return "USER_NOT_EXISTS"

    # có thì kiểm tra mật khẩu có đúng không
    if not verify_password(login_inp.password, user.hashed_password):
        return "INCORRECT_PASSWORD"

    # đăng nhập được thì cấp token
    payload = {
        "sub": user.id,
        "username": user.username,
        "role": user.role
    }

    token = create_access_token(payload)

    return token


# =============================== END REGION ===============================


# giải mã payload token
# def decode_access_token(token: str) -> dict | None:

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         return payload
#     except ExpiredSignatureError:
#         print("Lỗi: Token đã hết hạn")
#         return None
#     except InvalidTokenError:
#         print("Lỗi: Token không hợp lệ hoặc sai chữ ký")
#         return None
