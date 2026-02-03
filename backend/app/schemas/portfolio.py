from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.portfolio import CostMethod


class PortfolioBase(BaseModel):
    name: str
    base_currency: str = "TWD"
    cost_method: CostMethod = CostMethod.AVG


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = None
    base_currency: str | None = None
    cost_method: CostMethod | None = None


class PortfolioRead(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
