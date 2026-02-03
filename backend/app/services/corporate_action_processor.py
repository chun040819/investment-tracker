from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cash_transaction import CashTransaction, CashTxnType
from app.models.corporate_action import CorporateAction, CorporateActionType
from app.models.position_snapshot import PositionSnapshot
from app.models.price_history import PriceHistory
from app.models.trade import Trade, TradeSide
from app.services.cash_ledger_service import build_trade_expense_txn, get_cash_balance
from app.services.unit_of_work import UnitOfWork


def process_corporate_action(db: Session, action_id: int) -> dict:
    action = db.get(CorporateAction, action_id)
    if not action:
        raise ValueError("Corporate action not found")
    if action.processed_at is not None:
        raise ValueError("Corporate action already processed")

    with UnitOfWork(db):
        if action.type == CorporateActionType.DRIP:
            trades_created = _apply_drip(db, action)
        else:
            trades_created = _apply_split_like(db, action)
        action.processed_at = datetime.now(timezone.utc)

    return {
        "action_id": action.id,
        "type": action.type.value,
        "trades_created": trades_created,
    }


def _apply_split_like(db: Session, action: CorporateAction) -> int:
    ratio = Decimal(action.numerator) / Decimal(action.denominator)
    if ratio <= 0:
        raise ValueError("Split ratio must be positive")

    trades = (
        db.execute(
            select(Trade)
            .where(
                Trade.asset_id == action.asset_id,
                Trade.trade_date < action.date,
            )
            .order_by(Trade.trade_date, Trade.id)
        )
        .scalars()
        .all()
    )
    for trade in trades:
        trade.quantity *= ratio
        trade.price /= ratio

    stock_divs = (
        db.execute(
            select(CashTransaction).where(
                CashTransaction.asset_id == action.asset_id,
                CashTransaction.type == CashTxnType.DIVIDEND_STOCK,
                CashTransaction.date < action.date,
            )
        )
        .scalars()
        .all()
    )
    for div in stock_divs:
        if div.shares is not None:
            div.shares *= ratio

    snapshots = (
        db.execute(
            select(PositionSnapshot).where(
                PositionSnapshot.asset_id == action.asset_id,
                PositionSnapshot.snapshot_date < action.date,
            )
        )
        .scalars()
        .all()
    )
    for snap in snapshots:
        snap.shares *= ratio

    return 0


def _apply_drip(db: Session, action: CorporateAction) -> int:
    price = _get_price_on_or_before(db, action.asset_id, action.date)
    if price is None:
        raise ValueError("No price history found for DRIP date")

    cash_divs = (
        db.execute(
            select(CashTransaction).where(
                CashTransaction.asset_id == action.asset_id,
                CashTransaction.type == CashTxnType.DIVIDEND_CASH,
                CashTransaction.date == action.date,
            )
        )
        .scalars()
        .all()
    )

    trades_created = 0
    for div in cash_divs:
        if div.asset_id is None:
            continue
        reinvest_amount = div.amount - div.withholding_tax
        if reinvest_amount <= 0:
            continue

        balance = get_cash_balance(db, div.account_id, div.date)
        if balance < reinvest_amount:
            raise ValueError("Insufficient cash balance for DRIP")

        quantity = reinvest_amount / price
        trade = Trade(
            portfolio_id=div.portfolio_id,
            account_id=div.account_id,
            asset_id=div.asset_id,
            trade_date=div.date,
            side=TradeSide.BUY,
            quantity=quantity,
            price=price,
            fee=Decimal("0"),
            tax=Decimal("0"),
            currency=div.asset.currency if div.asset else None,
            note=f"DRIP from cash txn {div.id}",
        )
        db.add(trade)
        db.add(build_trade_expense_txn(trade))
        trades_created += 1

    return trades_created


def _get_price_on_or_before(db: Session, asset_id: int, as_of: date | None) -> Decimal | None:
    if as_of is None:
        return None
    price = (
        db.execute(
            select(PriceHistory)
            .where(PriceHistory.asset_id == asset_id, PriceHistory.date <= as_of)
            .order_by(PriceHistory.date.desc(), PriceHistory.id.desc())
            .limit(1)
        )
        .scalars()
        .first()
    )
    return price.close if price else None
