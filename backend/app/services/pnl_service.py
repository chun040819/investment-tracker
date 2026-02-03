from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trade import Trade, TradeSide
from app.models.cash_transaction import CashTransaction, CashTxnType
from app.models.price_history import PriceHistory
from app.models.asset import Asset
from app.models.corporate_action import CorporateAction


class HoldingState:
    def __init__(self, asset: Asset):
        self.asset = asset
        self.shares: Decimal = Decimal("0")
        self.cost_basis: Decimal = Decimal("0")

    @property
    def avg_cost(self) -> Decimal:
        return self.cost_basis / self.shares if self.shares > 0 else Decimal("0")


def _last_prices(db: Session, asset_ids: list[int], as_of: date) -> Dict[int, Decimal | None]:
    if not asset_ids:
        return {}
    stmt = (
        select(PriceHistory)
        .where(PriceHistory.asset_id.in_(asset_ids), PriceHistory.date <= as_of)
        .order_by(PriceHistory.asset_id, PriceHistory.date.desc())
    )
    prices: Dict[int, Decimal | None] = {}
    for ph in db.execute(stmt).scalars():
        if ph.asset_id not in prices:
            prices[ph.asset_id] = ph.close
    return prices


def compute_pnl_summary(
    db: Session,
    portfolio_id: int,
    from_date: date,
    to_date: date,
    as_of: date | None = None,
) -> dict:
    if as_of is None:
        as_of = datetime.now(timezone.utc).date()

    trades: list[Trade] = db.execute(
        select(Trade)
        .where(Trade.portfolio_id == portfolio_id, Trade.trade_date <= as_of)
        .order_by(Trade.trade_date, Trade.id)
    ).scalars().all()

    actions: list[CorporateAction] = db.execute(
        select(CorporateAction)
        .join(Asset)
        .where(
            Asset.id == CorporateAction.asset_id,
            CorporateAction.processed_at.is_(None),
            CorporateAction.date <= as_of,
        )
        .order_by(CorporateAction.date, CorporateAction.id)
    ).scalars().all()

    stock_dividends: list[CashTransaction] = db.execute(
        select(CashTransaction)
        .where(
            CashTransaction.portfolio_id == portfolio_id,
            CashTransaction.type == CashTxnType.DIVIDEND_STOCK,
            CashTransaction.date <= as_of,
        )
        .order_by(CashTransaction.date, CashTransaction.id)
    ).scalars().all()

    holdings: Dict[int, HoldingState] = {}
    realized = Decimal("0")

    timeline = []
    for act in actions:
        timeline.append((act.date, 0, "action", act))
    for div in stock_dividends:
        timeline.append((div.date, 1, "stock_div", div))
    for tr in trades:
        timeline.append((tr.trade_date, 2, "trade", tr))
    timeline.sort(key=lambda x: (x[0], x[1]))

    for _, _, kind, obj in timeline:
        if kind == "action":
            act: CorporateAction = obj
            asset = act.asset
            if asset.id not in holdings:
                holdings[asset.id] = HoldingState(asset)
            h = holdings[asset.id]
            ratio = Decimal(act.numerator) / Decimal(act.denominator)
            h.shares *= ratio
            if h.shares <= 0:
                h.cost_basis = Decimal("0")
        elif kind == "stock_div":
            div: CashTransaction = obj
            if div.shares is None or div.shares <= 0:
                continue
            asset = div.asset
            if asset is None:
                continue
            if asset.id not in holdings:
                holdings[asset.id] = HoldingState(asset)
            h = holdings[asset.id]
            h.shares += div.shares
            if h.shares <= 0:
                h.cost_basis = Decimal("0")
        else:
            trade: Trade = obj
            asset = trade.asset
            if asset.id not in holdings:
                holdings[asset.id] = HoldingState(asset)
            h = holdings[asset.id]

            if trade.side == TradeSide.BUY:
                total_cost = trade.quantity * trade.price + trade.fee + trade.tax
                h.cost_basis += total_cost
                h.shares += trade.quantity
            elif trade.side == TradeSide.SELL:
                avg_cost_now = h.avg_cost
                proceeds = trade.quantity * trade.price - trade.fee - trade.tax
                if from_date <= trade.trade_date <= to_date:
                    realized += proceeds - (avg_cost_now * trade.quantity)
                h.cost_basis -= avg_cost_now * trade.quantity
                h.shares -= trade.quantity
                if h.shares <= 0:
                    h.shares = Decimal("0")
                    h.cost_basis = Decimal("0")

    # Income
    income_types = {
        CashTxnType.DIVIDEND_CASH,
        CashTxnType.REWARD,
        CashTxnType.INTEREST,
        CashTxnType.FEE_REBATE,
        CashTxnType.TAX_REFUND,
        CashTxnType.OTHER,
    }
    income_dividend = Decimal("0")
    income_reward = Decimal("0")
    income_other = Decimal("0")

    cash_txns: list[CashTransaction] = (
        db.execute(
            select(CashTransaction).where(
                CashTransaction.portfolio_id == portfolio_id,
                CashTransaction.date >= from_date,
                CashTransaction.date <= to_date,
            )
        )
        .scalars()
        .all()
    )
    invested_cashflow = Decimal("0")
    for tx in cash_txns:
        if tx.type in income_types:
            if tx.type == CashTxnType.DIVIDEND_CASH:
                income_dividend += tx.amount - tx.withholding_tax
            elif tx.type in {CashTxnType.REWARD, CashTxnType.FEE_REBATE, CashTxnType.TAX_REFUND}:
                income_reward += tx.amount
            else:
                income_other += tx.amount
        elif tx.type in {CashTxnType.DEPOSIT, CashTxnType.WITHDRAW}:
            invested_cashflow += tx.amount

    income_total = income_dividend + income_reward + income_other

    # Unrealized as of
    last_prices = _last_prices(db, list(holdings.keys()), as_of)
    unrealized = Decimal("0")
    for asset_id, h in holdings.items():
        lp = last_prices.get(asset_id)
        if lp is not None and h.shares > 0:
            market_value = h.shares * lp
            unrealized += market_value - h.cost_basis

    price_return = realized + unrealized
    total_return = price_return + income_total

    return {
        "realized_pnl": realized,
        "income_total": income_total,
        "income_dividend": income_dividend,
        "income_reward": income_reward,
        "unrealized_pnl": unrealized,
        "price_return": price_return,
        "total_return": total_return,
        "invested_cashflow": invested_cashflow,
    }
