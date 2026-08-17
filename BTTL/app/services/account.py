import bcrypt
import jwt
import os
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from datetime import datetime, timedelta
from dotenv import load_dotenv


def transfer_money_sv(payload: TransferRequest, current_user_db: dict, db: Session):

    # current_user_check = current_user_db.get("username")
    # # loại trừ người chuyển là 1
    # if current_user_check == payload.to_username.lower():
    #     return "DUPLICATED_USERNAME_IN_TRANSFER"

    # người nhận

    print(current_user_db)
    sender = db.query(UserModel).filter(
        UserModel.id == current_user_db.get("sub")).first()

    # người chuyển
    receiver = db.query(UserModel).filter(
        UserModel.username == payload.to_username.lower()).first()

    if not receiver:
        return "RECIPIENT_NOT_FOUND"

    if sender.username == receiver.username:
        return "DUPLICATED_USERNAME_IN_TRANSFER"

    # ổn thì thì chuyển
    # kiểm tra xem số dư có đủ không
    if sender.balance < payload.amount:
        return "INSUFFICIENT_BALANCE "

    # ỔN THÌ CHUYỂN
    try:
        sender.balance -= payload.amount
        receiver.balance += payload.amount

        db.commit()

        return True

    except Exception as e:
        raise e
        db.rollback()
