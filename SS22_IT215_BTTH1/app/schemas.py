from pydantic import BaseModel, Field
from datetime import datetime

# Schema nhận dữ liệu đăng ký
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Tên đăng nhập")
    password: str = Field(..., min_length=6, description="Mật khẩu thô")

# Schema nhận dữ liệu đăng nhập
class UserLoginRequest(BaseModel):
    username: str
    password: str

# Schema trả về thông tin User (Tuyệt đối không trả hashed_password)
class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

# Schema trả về Access Token sau khi login thành công
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"