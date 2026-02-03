from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.trade import TradeSide
from app.schemas.tag import TagRead


def _decimal_to_str(val: Decimal) -> str:
    return format(val, "f")


class TradeBase(BaseModel):
    portfolio_id: int
    account_id: int
    asset_id: int
    trade_date: date
    side: TradeSide
    quantity: Decimal = Field(...)
    price: Decimal = Field(...)
    fee: Decimal = Field(default=Decimal("0"))
    tax: Decimal = Field(default=Decimal("0"))
    note: Optional[str] = None
    currency: Optional[str] = None
    asset_currency: Optional[str] = None
    settlement_currency: Optional[str] = None
    fx_rate: Optional[Decimal] = None
    tags: Optional[list[str]] = None

    @field_validator("quantity", "price", "fee", "tax")
    @classmethod
    def non_negative(cls, v: Decimal, info):  # type: ignore[override]
        if v < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v

    @field_validator("fx_rate")
    @classmethod
    def positive_fx(cls, v: Optional[Decimal]):  # type: ignore[override]
        if v is not None and v <= 0:
            raise ValueError("fx_rate must be positive")
        return v


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    trade_date: Optional[date] = None
    side: Optional[TradeSide] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    fee: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    note: Optional[str] = None
    currency: Optional[str] = None
    asset_currency: Optional[str] = None
    settlement_currency: Optional[str] = None
    fx_rate: Optional[Decimal] = None

    @field_validator("quantity", "price", "fee", "tax")
    @classmethod
    def non_negative(cls, v: Optional[Decimal], info):  # type: ignore[override]
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v

    @field_validator("fx_rate")
    @classmethod
    def positive_fx(cls, v: Optional[Decimal]):  # type: ignore[override]
        if v is not None and v <= 0:
            raise ValueError("fx_rate must be positive")
        return v


class TradeRead(TradeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: Optional[list[TagRead]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={Decimal: _decimal_to_str},
    )
