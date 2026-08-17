from fastapi import FastAPI
from app.models import *
from app.models import *
from app.routers.auth import auth_routers
from app.routers.account import account_router
from app.routers.admin import admin_routers
from app.database import Base, Engine

app = FastAPI()

Base.metadata.create_all(Engine)


app.include_router(auth_routers)
app.include_router(account_router)
app.include_router(admin_routers)
