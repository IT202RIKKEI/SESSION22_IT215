import bcrypt
import jwt
import os
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models import UserModel
from app.schemas import UserRegisterRequest, UserLoginRequest
from datetime import datetime, timedelta
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

SECRET_KEY = os.getenv("SECRET_KEY", "devconnect_super_secret_jwt_key_2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

security = HTTPBearer()


def get_current_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Bắt lỗi khi token quá hạn
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn. Vui lòng đăng nhập lại!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        # Bắt lỗi khi token giả mạo, sai secret key hoặc sai định dạng
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ!",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    # TODO: Tự viết logic bcrypt.gensalt() và bcrypt.hashpw()

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # TODO: Tự viết logic bcrypt.checkpw()
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict) -> str:
    # TODO: Tự viết logic gán exp và jwt.encode()

    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire_time})

    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def register_user(user_in: UserRegisterRequest, db: Session):
    # Kiểm tra xem username đã tồn tại trong DB chưa
    existing_user = db.query(UserModel).filter(
        UserModel.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại trên hệ thống"
        )

    # Băm mật khẩu thô
    hashed_pwd = hash_password(user_in.password)

    # Tạo bản ghi User mới
    new_user = UserModel(
        username=user_in.username,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =============================== 5. LOGIC ĐĂNG NHẬP ===============================
def authenticate_user(login_in: UserLoginRequest, db: Session):
    # Truy vấn user theo username
    user = db.query(UserModel).filter(
        UserModel.username == login_in.username).first()

    # Kiểm tra: nếu user không tồn tại HOẶC mật khẩu sai -> báo lỗi 401 chung chung
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # TODO: [BẠN TỰ VIẾT PHẦN CẤP TOKEN DƯỚI ĐÂY]
    payload = {
        "sub": str(user.id),
        "username": user.username
    }
    token = create_access_token(payload)

    return {
        "access_token": token,
        "token_type": "bearer"
    }



