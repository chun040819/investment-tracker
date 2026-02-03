from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeRead, TradeUpdate
from app.routers.utils import handle_integrity_error
from app.models.tag import Tag
from app.models.asset import Asset
from app.models.account import Account
from app.models.fx_rate import FXRate
from app.services.cash_ledger_service import build_trade_expense_txn, get_cash_balance, trade_total_cost
from app.services.cache import cache_delete_pattern
from app.services.tax_lot_service import rebuild_tax_lots
from app.services.unit_of_work import UnitOfWork

router = APIRouter(prefix="/trades", tags=["trades"])


def _upsert_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    tags: list[Tag] = []
    for name in tag_names:
        existing = db.execute(select(Tag).where(Tag.name == name)).scalars().first()
        if existing:
            tags.append(existing)
        else:
            new_tag = Tag(name=name)
            db.add(new_tag)
            tags.append(new_tag)
    return tags


def _resolve_fx_rate(db: Session, from_currency: str, to_currency: str, as_of: date) -> Decimal | None:
    fx = (
        db.execute(
            select(FXRate)
            .where(
                FXRate.from_currency == from_currency,
                FXRate.to_currency == to_currency,
                FXRate.date <= as_of,
            )
            .order_by(FXRate.date.desc(), FXRate.id.desc())
            .limit(1)
        )
        .scalars()
        .first()
    )
    return fx.rate if fx else None


def _normalize_trade_currencies(db: Session, data: dict) -> None:
    asset = db.get(Asset, data["asset_id"])
    account = db.get(Account, data["account_id"])

    if not data.get("asset_currency"):
        if data.get("currency"):
            data["asset_currency"] = data["currency"]
        else:
            data["asset_currency"] = asset.currency if asset else None

    if not data.get("settlement_currency"):
        data["settlement_currency"] = account.currency if account else data.get("asset_currency")

    if not data.get("currency"):
        data["currency"] = data.get("asset_currency")

    if account and data["settlement_currency"] != account.currency:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Settlement currency must match account")

    asset_ccy = data.get("asset_currency")
    settle_ccy = data.get("settlement_currency")
    if asset_ccy and settle_ccy and asset_ccy != settle_ccy:
        if data.get("fx_rate") is None:
            rate = _resolve_fx_rate(db, asset_ccy, settle_ccy, data["trade_date"])
            if rate is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="FX rate required for settlement")
            data["fx_rate"] = rate


def _available_shares(db: Session, portfolio_id: int, asset_id: int, up_to: date, exclude_trade_id: int | None = None) -> Decimal:
    from app.models.corporate_action import CorporateAction
    from app.models.cash_transaction import CashTransaction, CashTxnType
    from app.models.trade import Trade, TradeSide
    from app.models.asset import Asset

    # Collect events up to (and including) up_to
    trades = db.execute(
        select(Trade)
        .where(Trade.portfolio_id == portfolio_id, Trade.asset_id == asset_id, Trade.trade_date <= up_to)
        .order_by(Trade.trade_date, Trade.id)
    ).scalars().all()
    actions = db.execute(
        select(CorporateAction)
        .where(
            CorporateAction.asset_id == asset_id,
            CorporateAction.processed_at.is_(None),
            CorporateAction.date <= up_to,
        )
        .order_by(CorporateAction.date, CorporateAction.id)
    ).scalars().all()
    stock_divs = db.execute(
        select(CashTransaction)
        .where(
            CashTransaction.portfolio_id == portfolio_id,
            CashTransaction.asset_id == asset_id,
            CashTransaction.type == CashTxnType.DIVIDEND_STOCK,
            CashTransaction.date <= up_to,
        )
        .order_by(CashTransaction.date, CashTransaction.id)
    ).scalars().all()

    timeline = []
    for act in actions:
        timeline.append((act.date, 0, "action", act))
    for div in stock_divs:
        timeline.append((div.date, 1, "stock_div", div))
    for tr in trades:
        if exclude_trade_id is not None and tr.id == exclude_trade_id:
            continue
        timeline.append((tr.trade_date, 2, "trade", tr))
    timeline.sort(key=lambda x: (x[0], x[1]))

    shares = Decimal("0")
    for _, _, kind, obj in timeline:
        if kind == "action":
            act = obj
            ratio = Decimal(act.numerator) / Decimal(act.denominator)
            shares *= ratio
        elif kind == "stock_div":
            div = obj
            if div.shares:
                shares += div.shares
        else:
            tr = obj
            if tr.side == TradeSide.BUY:
                shares += tr.quantity
            else:
                shares -= tr.quantity
    return shares


@router.get("", response_model=list[TradeRead])
def list_trades(
    portfolio_id: int | None = Query(default=None),
    asset_id: int | None = Query(default=None),
    account_id: int | None = Query(default=None),
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
) -> list[Trade]:
    stmt = select(Trade)
    conditions = []
    if portfolio_id is not None:
        conditions.append(Trade.portfolio_id == portfolio_id)
    if asset_id is not None:
        conditions.append(Trade.asset_id == asset_id)
    if account_id is not None:
        conditions.append(Trade.account_id == account_id)
    if from_date is not None:
        conditions.append(Trade.trade_date >= from_date)
    if to_date is not None:
        conditions.append(Trade.trade_date <= to_date)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(Trade.trade_date)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=TradeRead, status_code=status.HTTP_201_CREATED)
def create_trade(payload: TradeCreate, db: Session = Depends(get_db)) -> Trade:
    data = payload.model_dump()
    tag_names = data.pop("tags", None)
    _normalize_trade_currencies(db, data)
    trade = Trade(**data)
    if tag_names:
        trade.tags = _upsert_tags(db, tag_names)
    if trade.side == trade.side.SELL:
        available = _available_shares(db, trade.portfolio_id, trade.asset_id, trade.trade_date)
        if trade.quantity > available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sell quantity exceeds available shares")
    if trade.side == trade.side.BUY:
        total_cost = trade_total_cost(trade)
        balance = get_cash_balance(db, trade.account_id, trade.trade_date)
        if balance < total_cost:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient cash balance")
    try:
        with UnitOfWork(db):
            db.add(trade)
            db.flush()
            if trade.side == trade.side.BUY:
                db.add(build_trade_expense_txn(trade))
            rebuild_tax_lots(db, trade.portfolio_id, trade.asset_id)
    except IntegrityError as exc:
        handle_integrity_error(exc, "Trade")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    cache_delete_pattern(f"cache:portfolio:{trade.portfolio_id}:*")
    db.refresh(trade)
    return trade


@router.put("/{trade_id}", response_model=TradeRead)
def update_trade(trade_id: int, payload: TradeUpdate, db: Session = Depends(get_db)) -> Trade:
    trade = db.get(Trade, trade_id)
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found")

    data = payload.model_dump(exclude_unset=True)
    tag_names = data.pop("tags", None)
    for field, value in data.items():
        setattr(trade, field, value)
    if tag_names is not None:
        trade.tags = _upsert_tags(db, tag_names)

    if any(
        key in data
        for key in {
            "asset_currency",
            "settlement_currency",
            "fx_rate",
            "currency",
            "trade_date",
            "asset_id",
            "account_id",
        }
    ):
        normalized = {
            "asset_id": trade.asset_id,
            "account_id": trade.account_id,
            "trade_date": trade.trade_date,
            "asset_currency": trade.asset_currency,
            "settlement_currency": trade.settlement_currency,
            "fx_rate": trade.fx_rate,
            "currency": trade.currency,
        }
        _normalize_trade_currencies(db, normalized)
        trade.asset_currency = normalized.get("asset_currency")
        trade.settlement_currency = normalized.get("settlement_currency")
        trade.fx_rate = normalized.get("fx_rate")
        trade.currency = normalized.get("currency")

    if trade.side == trade.side.SELL:
        available = _available_shares(db, trade.portfolio_id, trade.asset_id, trade.trade_date, exclude_trade_id=trade.id)
        if trade.quantity > available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sell quantity exceeds available shares")

    try:
        with UnitOfWork(db):
            db.flush()
            rebuild_tax_lots(db, trade.portfolio_id, trade.asset_id)
    except IntegrityError as exc:
        handle_integrity_error(exc, "Trade")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    cache_delete_pattern(f"cache:portfolio:{trade.portfolio_id}:*")
    db.refresh(trade)
    return trade


@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trade(trade_id: int, db: Session = Depends(get_db)) -> None:
    trade = db.get(Trade, trade_id)
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found")
    portfolio_id = trade.portfolio_id
    asset_id = trade.asset_id
    try:
        with UnitOfWork(db):
            db.delete(trade)
            db.flush()
            rebuild_tax_lots(db, portfolio_id, asset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    cache_delete_pattern(f"cache:portfolio:{portfolio_id}:*")
    return None
