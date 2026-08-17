from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from app.database import Engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from app.services.account import *
# giải mã và bắt token expired
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "trustbank_super_secret_jwt_key_2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


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
        # print(f"👉 DEBUG LỖI DECODE: {type(e).__name__} - {e}")
        raise credentials_exception


account_router = APIRouter(
    prefix="/account",
    tags=["QUẢN LÝ TÀI KHOẢN"],
    dependencies=[Depends(get_current_payload)]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =============================== REGION ===============================


@account_router.get("/balance", status_code=status.HTTP_200_OK)
def get_token_info(payload: dict = Depends(get_current_payload)):

    return {
        "message": "CHÀO MỪNG QUÝ KHÁCH",
        "payload_data": payload
    }
# =============================== END REGION ===============================


@account_router.post("/transfer", status_code=status.HTTP_200_OK)
def transfer_money(payload: TransferRequest, current_user: dict = Depends(get_current_payload), db: Session = Depends(get_db)):

    try:
        result = transfer_money_sv(payload, current_user, db)

        if result == "DUPLICATED_USERNAME_IN_TRANSFER":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không được gửi cho chính mình"
            )

        if result == "INSUFFICIENT_BALANCE ":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không đủ tiền để chuyển"
            )

        if result == "RECIPIENT_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Người nhận không tồn tại")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Có lỗi: {str(e)}"
        )
