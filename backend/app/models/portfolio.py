from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List

from sqlalchemy import DateTime, Enum as SQLEnum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CostMethod(str, Enum):
    AVG = "AVG"
    FIFO = "FIFO"


class Portfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = (UniqueConstraint("name", name="uq_portfolio_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    base_currency: Mapped[str] = mapped_column(String(10), default="TWD", nullable=False)
    cost_method: Mapped[CostMethod] = mapped_column(
        SQLEnum(CostMethod, name="cost_method_enum", validate_strings=True),
        default=CostMethod.AVG,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    accounts: Mapped[List["Account"]] = relationship(
        "Account", back_populates="portfolio", cascade="all, delete-orphan"
    )
    trades: Mapped[List["Trade"]] = relationship("Trade", back_populates="portfolio")
    cash_transactions: Mapped[List["CashTransaction"]] = relationship(
        "CashTransaction", back_populates="portfolio"
    )
