from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, UniqueConstraint, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaxLot(Base):
    __tablename__ = "tax_lots"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "asset_id", "source", "source_id", name="uq_tax_lot_source"),
        Index("ix_tax_lot_portfolio_asset_date", "portfolio_id", "asset_id", "lot_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    lot_date: Mapped[date] = mapped_column(Date, nullable=False)

    original_shares: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    remaining_shares: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    cost_per_share: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)

    asset_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    settlement_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    fx_rate: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)

    source: Mapped[str] = mapped_column(String(20), nullable=False)  # BUY | STOCK_DIV
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    portfolio = relationship("Portfolio")
    account = relationship("Account")
    asset = relationship("Asset")
