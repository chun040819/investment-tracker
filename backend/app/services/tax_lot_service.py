from __future__ import annotations

from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.cash_transaction import CashTransaction, CashTxnType
from app.models.corporate_action import CorporateAction
from app.models.tax_lot import TaxLot
from app.models.trade import Trade, TradeSide


def rebuild_tax_lots(db: Session, portfolio_id: int, asset_id: int) -> list[TaxLot]:
    db.execute(
        delete(TaxLot).where(TaxLot.portfolio_id == portfolio_id, TaxLot.asset_id == asset_id)
    )

    asset = db.get(Asset, asset_id)
    asset_currency = asset.currency if asset else None

    trades = (
        db.execute(
            select(Trade)
            .where(Trade.portfolio_id == portfolio_id, Trade.asset_id == asset_id)
            .order_by(Trade.trade_date, Trade.id)
        )
        .scalars()
        .all()
    )

    actions = (
        db.execute(
            select(CorporateAction)
            .where(
                CorporateAction.asset_id == asset_id,
                CorporateAction.processed_at.is_(None),
            )
            .order_by(CorporateAction.date, CorporateAction.id)
        )
        .scalars()
        .all()
    )

    stock_divs = (
        db.execute(
            select(CashTransaction)
            .where(
                CashTransaction.portfolio_id == portfolio_id,
                CashTransaction.asset_id == asset_id,
                CashTransaction.type == CashTxnType.DIVIDEND_STOCK,
            )
            .order_by(CashTransaction.date, CashTransaction.id)
        )
        .scalars()
        .all()
    )

    timeline = []
    for act in actions:
        timeline.append((act.date, 0, "action", act))
    for div in stock_divs:
        timeline.append((div.date, 1, "stock_div", div))
    for tr in trades:
        timeline.append((tr.trade_date, 2, "trade", tr))
    timeline.sort(key=lambda x: (x[0], x[1]))

    lots: list[TaxLot] = []

    for _, _, kind, obj in timeline:
        if kind == "action":
            act = obj
            ratio = Decimal(act.numerator) / Decimal(act.denominator)
            if ratio <= 0:
                continue
            for lot in lots:
                lot.original_shares *= ratio
                lot.remaining_shares *= ratio
                if lot.original_shares > 0:
                    lot.cost_per_share = lot.total_cost / lot.original_shares
                else:
                    lot.cost_per_share = Decimal("0")
        elif kind == "stock_div":
            div = obj
            if div.shares is None or div.shares <= 0:
                continue
            lot = TaxLot(
                portfolio_id=div.portfolio_id,
                account_id=div.account_id,
                asset_id=div.asset_id,
                lot_date=div.date,
                original_shares=div.shares,
                remaining_shares=div.shares,
                cost_per_share=Decimal("0"),
                total_cost=Decimal("0"),
                asset_currency=asset_currency,
                settlement_currency=div.account.currency if div.account else None,
                fx_rate=None,
                source="STOCK_DIV",
                source_id=div.id,
            )
            lots.append(lot)
        else:
            tr = obj
            if tr.side == TradeSide.BUY:
                total_cost = tr.quantity * tr.price + tr.fee + tr.tax
                cost_per_share = total_cost / tr.quantity if tr.quantity > 0 else Decimal("0")
                lot = TaxLot(
                    portfolio_id=tr.portfolio_id,
                    account_id=tr.account_id,
                    asset_id=tr.asset_id,
                    lot_date=tr.trade_date,
                    original_shares=tr.quantity,
                    remaining_shares=tr.quantity,
                    cost_per_share=cost_per_share,
                    total_cost=total_cost,
                    asset_currency=tr.asset_currency or asset_currency,
                    settlement_currency=tr.settlement_currency,
                    fx_rate=tr.fx_rate,
                    source="BUY",
                    source_id=tr.id,
                )
                lots.append(lot)
            else:
                remaining = tr.quantity
                for lot in lots:
                    if remaining <= 0:
                        break
                    if lot.remaining_shares <= 0:
                        continue
                    take = lot.remaining_shares if lot.remaining_shares <= remaining else remaining
                    lot.remaining_shares -= take
                    remaining -= take
                if remaining > 0:
                    raise ValueError("Sell quantity exceeds available lots")

    for lot in lots:
        db.add(lot)

    return lots
