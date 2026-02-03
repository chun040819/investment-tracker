from __future__ import annotations

from datetime import datetime, date, timezone
from decimal import Decimal
from enum import Enum
from typing import List

from sqlalchemy import Date, DateTime, Enum as SQLEnum, ForeignKey, Index, Numeric, String, Text, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TradeSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


trade_tag_table = Table(
    "trade_tags",
    Base.metadata,
    Column("trade_id", ForeignKey("trades.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Trade(Base):
    __tablename__ = "trades"
    __table_args__ = (
        Index("ix_trade_portfolio_date", "portfolio_id", "trade_date"),
        Index("ix_trade_asset_date", "asset_id", "trade_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    side: Mapped[TradeSide] = mapped_column(SQLEnum(TradeSide, name="trade_side_enum", validate_strings=True), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False, default=Decimal("0"))
    tax: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False, default=Decimal("0"))
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    asset_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    settlement_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    fx_rate: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="trades")
    account: Mapped["Account"] = relationship("Account", back_populates="trades")
    asset: Mapped["Asset"] = relationship("Asset", back_populates="trades")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary="trade_tags", back_populates="trades", cascade="all")
