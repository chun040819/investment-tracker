from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    name: str
    currency: str
    note: str | None = None


class AccountCreate(AccountBase):
    portfolio_id: int


class AccountUpdate(BaseModel):
    name: str | None = None
    currency: str | None = None
    note: str | None = None


class AccountRead(AccountBase):
    id: int
    portfolio_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
