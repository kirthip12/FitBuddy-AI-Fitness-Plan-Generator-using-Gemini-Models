from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
    func
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    goal: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    intensity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    experience_level: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="beginner"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


class Plan(Base):

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )