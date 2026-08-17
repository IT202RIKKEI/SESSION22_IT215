from pydantic import BaseModel, ConfigDict, Field, EmailStr
from enum import Enum
from datetime import datetime


class UserRole(str,Enum):

    CUSTOMER = "customer"
    ADMIN = "admin"


class UserRegisterRequest(BaseModel):

    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=3, max_length=20)
    role: UserRole = Field(default=UserRole.CUSTOMER)


class UserLoginRequest(BaseModel):

    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=3, max_length=20)


class ChangePasswordRequest(BaseModel):

    old_password: str = Field(min_length=3, max_length=20)
    new_password: str = Field(min_length=3, max_length=20)


class TransferRequest(BaseModel):

    to_username: str = Field(min_length=3, max_length=20)
    amount: float = Field(gt=0)
    note: str | None = "chuyen tien noi bo"


# phần response
class UserResponse(BaseModel):

    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponses(BaseModel):

    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int = 15


class BalanceResponse(BaseModel):
    username: str
    balance: float


class TransferResponse(BaseModel):
    success: bool
    message: str
    sender: str
    receiver: str
    amount: float
    current_balance: float


class UserAdminResponse(BaseModel):
    id: int
    username: str
    role: str
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True
