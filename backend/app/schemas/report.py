from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


def _d(val: Decimal) -> str:
    return format(val, "f")


class PositionOut(BaseModel):
    asset_id: int
    symbol: str
    name: str
    currency: str
    shares_held: Decimal
    avg_cost: Decimal
    cost_basis: Decimal
    last_price: Decimal | None
    market_value: Decimal | None
    unrealized_pnl: Decimal | None
    fx_rate_used: Optional[Decimal] = None
    market_value_base: Optional[Decimal] = None
    unrealized_pnl_base: Optional[Decimal] = None

    model_config = ConfigDict(json_encoders={Decimal: _d})


class PnLSummaryOut(BaseModel):
    realized_pnl: Decimal
    income_total: Decimal
    income_dividend: Decimal
    income_reward: Decimal
    unrealized_pnl: Decimal
    price_return: Decimal
    total_return: Decimal
    invested_cashflow: Decimal

    model_config = ConfigDict(json_encoders={Decimal: _d})
