from fastapi import APIRouter, status, HTTPException, Depends
from app.database import Engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from app.services.auth import *

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

        if token == "USER_NOT_EXISTS":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Người dùng {login_inp.username} không tồn tại"
            )

        if token == "INCORRECT_PASSWORD":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="tài khoản hoặc mật khẩu sai"
            )

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
