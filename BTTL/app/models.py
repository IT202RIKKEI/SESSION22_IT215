from sqlalchemy import String, Integer, Enum as PyEnum, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum
from datetime import datetime, timezone


class UserRole(str, enum.Enum):

    CUSTOMER = "customer"
    ADMIN = "admin"


class UserModel(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        PyEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=100000)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


