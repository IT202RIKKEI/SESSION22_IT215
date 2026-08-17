from fastapi import APIRouter, status, HTTPException, Depends
from app.database import Engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from app.services.auth import *
from app.routers.account import get_current_payload

auth_routers = APIRouter(
    prefix="/auth",
    tags=["Quản lý xác thực"]
)


@auth_routers.post("/register", status_code=status.HTTP_201_CREATED)
def user_register(user_inp: UserRegisterRequest, db: Session = Depends(get_db)):

    try:
        result = register_user_sv(user_inp, db)

        if result == "EXISTS_USERNAME":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Tên tài khoản đã tồn tại")
        safe_user_data = UserResponse.model_validate(result)

        return {
            "message": "Đăng kí tài khoản mới thành công",
            "data": safe_user_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Có lỗi hệ thống: {str(e)}"
        )


# =============================== ĐĂNG NHẬP CẤP PHÁT TOKEN  ===============================
@auth_routers.post("/login", status_code=status.HTTP_200_OK)
def user_login(login_inp: UserLoginRequest, db: Session = Depends(get_db)):

    try:
        token = user_login_sv(login_inp, db)
        return {
            "message": "đăng nhập thành công",
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Có lỗi hệ thống: {str(e)}"
        )


@auth_routers.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(old_password: str, new_password: str, payload: dict = Depends(get_current_payload), db: Session = Depends(get_db)):

    try:

        result = change_password_sv(old_password, new_password, payload, db)

        if result:
            return {
                "message": "ĐỔI MẬT KHẨU THÀNH CÔNG"
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Có lỗi hệ thống: {str(e)}"
        )
