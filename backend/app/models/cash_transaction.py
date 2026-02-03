from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import List

from sqlalchemy import Date, DateTime, Enum as SQLEnum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CashTxnType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    DIVIDEND_CASH = "DIVIDEND_CASH"
    DIVIDEND_STOCK = "DIVIDEND_STOCK"
    REWARD = "REWARD"
    INTEREST = "INTEREST"
    FEE_REBATE = "FEE_REBATE"
    TAX_REFUND = "TAX_REFUND"
    TRADE_EXPENSE = "TRADE_EXPENSE"
    OTHER = "OTHER"


class CashTransaction(Base):
    __tablename__ = "cash_transactions"
    __table_args__ = (Index("ix_cashtxn_portfolio_date", "portfolio_id", "date"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    asset_id: Mapped[int | None] = mapped_column(ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    type: Mapped[CashTxnType] = mapped_column(
        SQLEnum(CashTxnType, name="cash_txn_type_enum", validate_strings=True), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    withholding_tax: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False, default=Decimal("0"))
    shares: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
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

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="cash_transactions")
    account: Mapped["Account"] = relationship("Account", back_populates="cash_transactions")
    asset: Mapped["Asset"] = relationship("Asset", back_populates="cash_transactions")
