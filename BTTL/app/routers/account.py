from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from app.database import Engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from app.services.auth import *
# giải mã và bắt token expired
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "trustbank_secret_key_2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

account_router = APIRouter(
    prefix="/account",
    tags=["QUẢN LÝ TÀI KHOẢN"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise credentials_exception

# =============================== REGION ===============================


@account_router.get("/balance", status_code=status.HTTP_200_OK)
def get_token_info(payload: dict = Depends(get_current_payload)):

    return {
        "message": "CHÀO MỪNG QUÝ KHÁCH",
        "payload_data": payload
    }
# =============================== END REGION ===============================
