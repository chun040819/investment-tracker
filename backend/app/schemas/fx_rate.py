from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


def _d(val: Decimal) -> str:
    return format(val, "f")


class FXRateBase(BaseModel):
    date: date
    from_currency: str
    to_currency: str
    rate: Decimal


class FXRateCreate(FXRateBase):
    pass


class FXRateUpdate(BaseModel):
    date: Optional[date] = None
    from_currency: Optional[str] = None
    to_currency: Optional[str] = None
    rate: Optional[Decimal] = None


class FXRateRead(FXRateBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={Decimal: _d},
    )
