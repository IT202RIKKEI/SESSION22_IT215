import bcrypt
import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import os
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "trustbank_super_secret_jwt_key_2026")
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

    if not user or not verify_password(login_inp.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác"
        )

    # đăng nhập được thì cấp token
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "balance": str(user.balance)
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


# =============================== ĐỔI MẬT KHẨU ===============================
def change_password_sv(old_password: str, new_password: str, payload: dict, db: Session) -> bool:

    user_id = payload.get("sub")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    # kiểm tra mật khẩu có khớp với mật khẩu cũ không

    if not verify_password(old_password, user.hashed_password):

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mật khẩu cũ không đúng"
        )

    # nếu đúng thì cập nhật

    # hashed password mới
    new_hashed_password = hashed_password_sv(new_password)

    # cập nhật
    user.hashed_password = new_hashed_password

    db.commit()
    db.refresh(user)

    return True
