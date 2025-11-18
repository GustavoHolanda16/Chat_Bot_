from sqlalchemy import create_engine, Column, INTEGER, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os

os.makedirs("./db",exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/store.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()