from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cash_transaction import CashTransaction, CashTxnType
from app.models.trade import Trade


def get_cash_balance(db: Session, account_id: int, as_of: date) -> Decimal:
    total = (
        db.execute(
            select(func.coalesce(func.sum(CashTransaction.amount), 0)).where(
                CashTransaction.account_id == account_id,
                CashTransaction.date <= as_of,
            )
        )
        .scalars()
        .first()
    )
    if total is None:
        return Decimal("0")
    if isinstance(total, Decimal):
        return total
    return Decimal(str(total))


def trade_total_cost(trade: Trade) -> Decimal:
    total = trade.quantity * trade.price + trade.fee + trade.tax
    if (
        trade.fx_rate is not None
        and trade.asset_currency
        and trade.settlement_currency
        and trade.asset_currency != trade.settlement_currency
    ):
        return total * trade.fx_rate
    return total


def build_trade_expense_txn(trade: Trade) -> CashTransaction:
    total_cost = trade_total_cost(trade)
    return CashTransaction(
        portfolio_id=trade.portfolio_id,
        account_id=trade.account_id,
        asset_id=trade.asset_id,
        date=trade.trade_date,
        type=CashTxnType.TRADE_EXPENSE,
        amount=-total_cost,
        withholding_tax=Decimal("0"),
        shares=None,
        note="Auto trade expense",
    )
