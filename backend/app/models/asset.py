from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List

from sqlalchemy import DateTime, Enum as SQLEnum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AssetType(str, Enum):
    STOCK = "STOCK"
    ETF = "ETF"
    REIT = "REIT"
    OTHER = "OTHER"


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("symbol", "exchange", name="uq_asset_symbol_exchange"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(
        SQLEnum(AssetType, name="asset_type_enum", validate_strings=True), nullable=False
    )
    exchange: Mapped[str | None] = mapped_column(String(20), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    trades: Mapped[List["Trade"]] = relationship("Trade", back_populates="asset")
    corporate_actions: Mapped[List["CorporateAction"]] = relationship(
        "CorporateAction", back_populates="asset"
    )
    price_history: Mapped[List["PriceHistory"]] = relationship("PriceHistory", back_populates="asset")
    cash_transactions: Mapped[List["CashTransaction"]] = relationship(
        "CashTransaction", back_populates="asset"
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="asset_tags", back_populates="assets", cascade="all"
    )
