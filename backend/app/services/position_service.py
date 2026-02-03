from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trade import TradeSide, Trade
from app.models.price_history import PriceHistory
from app.models.asset import Asset
from app.models.corporate_action import CorporateAction
from app.models.cash_transaction import CashTransaction, CashTxnType
from app.models.fx_rate import FXRate
from app.models.portfolio import Portfolio
from app.models.position_snapshot import PositionSnapshot


class Position:
    def __init__(self, asset: Asset):
        self.asset = asset
        self.shares: Decimal = Decimal("0")
        self.cost_basis: Decimal = Decimal("0")
        self.realized_pnl: Decimal = Decimal("0")

    @property
    def avg_cost(self) -> Decimal:
        return self.cost_basis / self.shares if self.shares > 0 else Decimal("0")

    @classmethod
    def from_snapshot(cls, snap: PositionSnapshot) -> "Position":
        pos = cls(snap.asset)
        pos.shares = snap.shares
        pos.cost_basis = snap.cost_basis
        pos.realized_pnl = snap.realized_pnl
        return pos

def _get_last_prices(db: Session, asset_ids: list[int], as_of: date) -> dict[int, Decimal | None]:
    if not asset_ids:
        return {}
    stmt = (
        select(PriceHistory)
        .where(PriceHistory.asset_id.in_(asset_ids), PriceHistory.date <= as_of)
        .order_by(PriceHistory.asset_id, PriceHistory.date.desc())
    )
    prices: dict[int, Decimal | None] = {}
    for ph in db.execute(stmt).scalars():
        if ph.asset_id not in prices:
            prices[ph.asset_id] = ph.close
    return prices


def _get_fx_rate(db: Session, from_currency: str, to_currency: str, as_of: date) -> Decimal | None:
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


def _apply_corporate_action(pos: Position, action: CorporateAction) -> None:
    ratio = Decimal(action.numerator) / Decimal(action.denominator)
    # cost_basis unchanged; redistribute over new share count.
    pos.shares *= ratio
    if pos.shares > 0:
        # avg_cost recomputed through property when used; cost_basis unchanged.
        pass
    else:
        pos.cost_basis = Decimal("0")


def _latest_snapshot_date(db: Session, portfolio_id: int, as_of: date) -> date | None:
    return (
        db.execute(
            select(PositionSnapshot.snapshot_date)
            .where(PositionSnapshot.portfolio_id == portfolio_id, PositionSnapshot.snapshot_date <= as_of)
            .order_by(PositionSnapshot.snapshot_date.desc())
            .limit(1)
        )
        .scalars()
        .first()
    )


def _initial_positions_from_snapshot(db: Session, portfolio_id: int, as_of: date) -> tuple[dict[int, Position], date | None]:
    snap_date = _latest_snapshot_date(db, portfolio_id, as_of)
    if snap_date is None:
        return {}, None

    snapshots: list[PositionSnapshot] = (
        db.execute(
            select(PositionSnapshot)
            .where(
                PositionSnapshot.portfolio_id == portfolio_id,
                PositionSnapshot.snapshot_date == snap_date,
            )
            .order_by(PositionSnapshot.asset_id)
        )
        .scalars()
        .all()
    )
    positions: dict[int, Position] = {}
    for snap in snapshots:
        positions[snap.asset_id] = Position.from_snapshot(snap)
    return positions, snap_date


def get_positions(
    db: Session,
    portfolio_id: int,
    as_of: date | None = None,
    in_base_currency: bool = False,
    use_snapshots: bool = True,
    include_realized: bool = False,
) -> list[dict]:
    if as_of is None:
        as_of = datetime.now(timezone.utc).date()

    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio:
        return []

    positions: dict[int, Position]
    start_date: date | None
    if use_snapshots:
        positions, start_date = _initial_positions_from_snapshot(db, portfolio_id, as_of)
    else:
        positions, start_date = {}, None

    trade_filters = [Trade.portfolio_id == portfolio_id, Trade.trade_date <= as_of]
    if start_date:
        trade_filters.append(Trade.trade_date > start_date)
    trades: list[Trade] = (
        db.execute(select(Trade).where(*trade_filters).order_by(Trade.trade_date, Trade.id)).scalars().all()
    )

    action_filters = [CorporateAction.date <= as_of]
    if start_date:
        action_filters.append(CorporateAction.date > start_date)
    actions: list[CorporateAction] = (
        db.execute(
            select(CorporateAction)
            .join(Asset)
            .where(
                Asset.id == CorporateAction.asset_id,
                CorporateAction.processed_at.is_(None),
                *action_filters,
            )
            .order_by(CorporateAction.date, CorporateAction.id)
        )
        .scalars()
        .all()
    )

    stock_div_filters = [
        CashTransaction.portfolio_id == portfolio_id,
        CashTransaction.type == CashTxnType.DIVIDEND_STOCK,
        CashTransaction.date <= as_of,
    ]
    if start_date:
        stock_div_filters.append(CashTransaction.date > start_date)
    stock_dividends: list[CashTransaction] = (
        db.execute(
            select(CashTransaction)
            .where(*stock_div_filters)
            .order_by(CashTransaction.date, CashTransaction.id)
        )
        .scalars()
        .all()
    )

    # merge timeline: corporate actions -> stock dividends -> trades (same day order fixed)
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
            action: CorporateAction = obj
            asset = action.asset
            if asset.id not in positions:
                positions[asset.id] = Position(asset)
            _apply_corporate_action(positions[asset.id], action)
        elif kind == "stock_div":
            div: CashTransaction = obj
            if div.shares is None or div.shares <= 0:
                continue
            asset = div.asset
            if asset is None:
                continue
            if asset.id not in positions:
                positions[asset.id] = Position(asset)
            pos = positions[asset.id]
            pos.shares += div.shares
            # cost_basis unchanged; avg_cost derived from property
        else:
            trade: Trade = obj
            asset = trade.asset
            if asset.id not in positions:
                positions[asset.id] = Position(asset)
            pos = positions[asset.id]

            if trade.side == TradeSide.BUY:
                total_cost = trade.quantity * trade.price + trade.fee + trade.tax
                pos.cost_basis += total_cost
                pos.shares += trade.quantity
            elif trade.side == TradeSide.SELL:
                avg_cost_now = pos.avg_cost
                proceeds = trade.quantity * trade.price - trade.fee - trade.tax
                realized = proceeds - (avg_cost_now * trade.quantity)
                pos.realized_pnl += realized
                pos.cost_basis -= avg_cost_now * trade.quantity
                pos.shares -= trade.quantity
                if pos.shares <= 0:
                    pos.shares = Decimal("0")
                    pos.cost_basis = Decimal("0")

    last_prices = _get_last_prices(db, list(positions.keys()), as_of)

    results: list[dict] = []
    for asset_id, pos in positions.items():
        lp = last_prices.get(asset_id)
        market_value = None
        unrealized = None
        if lp is not None and pos.shares > 0:
            market_value = pos.shares * lp
            unrealized = market_value - pos.cost_basis

        fx_rate_used = None
        market_value_base = None
        unrealized_base = None
        if in_base_currency:
            if pos.asset.currency == portfolio.base_currency:
                fx_rate_used = Decimal("1")
            else:
                fx_rate_used = _get_fx_rate(db, pos.asset.currency, portfolio.base_currency, as_of)
            if fx_rate_used is not None and market_value is not None:
                market_value_base = market_value * fx_rate_used
                cost_basis_base = pos.cost_basis * fx_rate_used
                unrealized_base = market_value_base - cost_basis_base

        results.append(
            {
                "asset_id": asset_id,
                "symbol": pos.asset.symbol,
                "name": pos.asset.name,
                "currency": pos.asset.currency,
                "shares_held": pos.shares,
                "avg_cost": pos.avg_cost if pos.shares > 0 else Decimal("0"),
                "cost_basis": pos.cost_basis,
                "last_price": lp,
                "market_value": market_value,
                "unrealized_pnl": unrealized,
                "fx_rate_used": fx_rate_used,
                "market_value_base": market_value_base,
                "unrealized_pnl_base": unrealized_base,
                **({"realized_pnl": pos.realized_pnl} if include_realized else {}),
            }
        )

    return results
