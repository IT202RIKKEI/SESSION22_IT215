from fastapi import FastAPI
from app.database import Base, engine
from app.routers.auth import auth_router

# Tự động tạo bảng users nếu chưa có trong DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevConnect Authentication Service",
    version="1.0.0",
    description="Hệ thống xác thực an toàn với Bcrypt & Stateless JWT"
)

app.include_router(auth_router)


@app.get("/", tags=["ROOT"])
def root():
    return {"message": "DevConnect Auth API is running!"}
