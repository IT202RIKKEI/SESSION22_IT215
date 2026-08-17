import bcrypt
import jwt
import os
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from datetime import datetime, timedelta
from dotenv import load_dotenv


def admin_management_sv(payload_data: dict, db: Session):

    print(payload_data)
    # check role
    valid_role = payload_data.get("role") == "admin"

    if not valid_role:
        return "PERMISSION_DENIED"

    return db.query(UserModel).all()
