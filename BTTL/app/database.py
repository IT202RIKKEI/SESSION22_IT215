import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:01884814110Loc*@localhost:3306/student_db")

Engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=Engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
