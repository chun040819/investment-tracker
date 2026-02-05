from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_current_user
from app.db.session import get_db
from app.models.cash_transaction import CashTransaction, CashTxnType
from app.models.user import User
from app.schemas.cash_transaction import (
    CashTransactionCreate,
    CashTransactionRead,
    CashTransactionUpdate,
)
from app.routers.utils import handle_integrity_error
from app.services.cache import cache_delete_pattern

router = APIRouter(prefix="/cash-transactions", tags=["cash-transactions"])


def normalize_amount(txn_type: CashTxnType, amount: Decimal) -> Decimal:
    """Ensure DEPOSIT positive and WITHDRAW negative; others unchanged."""
    if txn_type == CashTxnType.DEPOSIT and amount < 0:
        return -amount
    if txn_type in {CashTxnType.WITHDRAW, CashTxnType.TRADE_EXPENSE} and amount > 0:
        return -amount
    return amount


@router.get("", response_model=list[CashTransactionRead])
def list_cash_transactions(
    portfolio_id: int | None = Query(default=None),
    type: CashTxnType | None = Query(default=None),
    asset_id: int | None = Query(default=None),
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CashTransaction]:
    stmt = select(CashTransaction)
    conditions = []
    if portfolio_id is not None:
        conditions.append(CashTransaction.portfolio_id == portfolio_id)
    if type is not None:
        conditions.append(CashTransaction.type == type)
    if asset_id is not None:
        conditions.append(CashTransaction.asset_id == asset_id)
    if from_date is not None:
        conditions.append(CashTransaction.date >= from_date)
    if to_date is not None:
        conditions.append(CashTransaction.date <= to_date)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(CashTransaction.date)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=CashTransactionRead, status_code=status.HTTP_201_CREATED)
def create_cash_transaction(
    payload: CashTransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CashTransaction:
    data = payload.model_dump()
    data["amount"] = normalize_amount(payload.type, data["amount"])
    txn = CashTransaction(**data)
    db.add(txn)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "CashTransaction")
    db.refresh(txn)
    cache_delete_pattern(f"cache:portfolio:{txn.portfolio_id}:*")
    return txn


@router.put("/{txn_id}", response_model=CashTransactionRead)
def update_cash_transaction(
    txn_id: int,
    payload: CashTransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CashTransaction:
    txn = db.get(CashTransaction, txn_id)
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cash transaction not found")

    updates = payload.model_dump(exclude_unset=True)
    if "amount" in updates or "type" in updates:
        txn_type = updates.get("type", txn.type)
        amount = updates.get("amount", txn.amount)
        updates["amount"] = normalize_amount(txn_type, amount)

    for field, value in updates.items():
        setattr(txn, field, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "CashTransaction")
    db.refresh(txn)
    cache_delete_pattern(f"cache:portfolio:{txn.portfolio_id}:*")
    return txn


@router.delete("/{txn_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cash_transaction(
    txn_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    txn = db.get(CashTransaction, txn_id)
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cash transaction not found")
    db.delete(txn)
    db.commit()
    cache_delete_pattern(f"cache:portfolio:{txn.portfolio_id}:*")
    return None
