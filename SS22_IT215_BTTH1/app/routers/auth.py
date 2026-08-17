from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from app.services.auth import register_user, authenticate_user
from app.services.auth import get_current_payload

auth_router = APIRouter(prefix="/api", tags=["AUTHENTICATION"])


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản DevConnect"
)
def register(user_in: UserRegisterRequest, db: Session = Depends(get_db)):
    return register_user(user_in=user_in, db=db)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập và nhận JWT Access Token"
)
def login(login_in: UserLoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(login_in=login_in, db=db)


@auth_router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(payload: dict = Depends(get_current_payload)):

    return {
        "message": "CHÀO MỪNG QUÝ KHÁCH",
        "data": payload
    }
