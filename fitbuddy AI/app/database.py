from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    DEFAULT_DATABASE_URL
)

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


def init_db():
    from . import models

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()