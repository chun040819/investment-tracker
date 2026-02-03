from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.asset import AssetType
from app.schemas.tag import TagRead


class AssetBase(BaseModel):
    symbol: str
    name: str
    asset_type: AssetType
    exchange: str | None = None
    currency: str = "USD"
    tags: list[str] | None = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: str | None = None
    asset_type: AssetType | None = None
    exchange: str | None = None
    currency: str | None = None


class AssetRead(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagRead] | None = None

    model_config = ConfigDict(from_attributes=True)
