# db/session.py
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///db/company.db"   # fallback for POC
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)
