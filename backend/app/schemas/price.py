from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


def _decimal_to_str(val: Decimal) -> str:
    return format(val, "f")


class PricePoint(BaseModel):
    date: date
    close: Decimal

    model_config = ConfigDict(json_encoders={Decimal: _decimal_to_str})


class PriceUpdateResult(BaseModel):
    inserted: int
    updated: int
