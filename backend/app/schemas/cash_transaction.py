from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.cash_transaction import CashTxnType


def _decimal_to_str(val: Decimal) -> str:
    return format(val, "f")


class CashTransactionBase(BaseModel):
    portfolio_id: int
    account_id: int
    asset_id: Optional[int] = None
    date: date
    type: CashTxnType
    amount: Decimal = Field(...)
    withholding_tax: Decimal = Field(default=Decimal("0"))
    shares: Optional[Decimal] = None
    note: Optional[str] = None

    @field_validator("withholding_tax")
    @classmethod
    def non_negative(cls, v: Decimal):  # type: ignore[override]
        if v < 0:
            raise ValueError("withholding_tax must be non-negative")
        return v


class CashTransactionCreate(CashTransactionBase):
    pass


class CashTransactionUpdate(BaseModel):
    date: Optional[date] = None
    type: Optional[CashTxnType] = None
    amount: Optional[Decimal] = None
    withholding_tax: Optional[Decimal] = None
    shares: Optional[Decimal] = None
    note: Optional[str] = None
    asset_id: Optional[int] = None

    @field_validator("withholding_tax")
    @classmethod
    def non_negative(cls, v: Optional[Decimal]):  # type: ignore[override]
        if v is not None and v < 0:
            raise ValueError("withholding_tax must be non-negative")
        return v


class CashTransactionRead(CashTransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={Decimal: _decimal_to_str},
    )
