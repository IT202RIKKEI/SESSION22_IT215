from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from app.database import Engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from app.routers.account import get_current_payload
from app.services.admin import *


admin_routers = APIRouter(
    prefix="/admin",
    tags=["QLADMIN"],
    dependencies=[Depends(get_current_payload)]
)


@admin_routers.get("/users", status_code=status.HTTP_200_OK)
def admin_managment(payload_data: dict = Depends(get_current_payload), db: Session = Depends(get_db)):

    try:
        result = admin_management_sv(payload_data, db)

        if result == "PERMISSION_DENIED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không có quyền truy cập"
            )

        return {
            "message": "admin lấy dữ liệu thành công",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Có lỗi hệ thống: {str(e)}"
        )
