from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.corporate_action import CorporateActionType


class CorporateActionBase(BaseModel):
    asset_id: int
    date: date
    type: CorporateActionType
    numerator: int
    denominator: int

    @field_validator("numerator", "denominator")
    @classmethod
    def positive(cls, v: int, info):
        if v <= 0:
            raise ValueError(f"{info.field_name} must be positive")
        return v

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, v):
        # accept MERGE as REVERSE_SPLIT for convenience
        if isinstance(v, str) and v.upper() == "MERGE":
            return CorporateActionType.REVERSE_SPLIT
        return v


class CorporateActionCreate(CorporateActionBase):
    pass


class CorporateActionUpdate(BaseModel):
    date: Optional[date] = None
    type: Optional[CorporateActionType] = None
    numerator: Optional[int] = None
    denominator: Optional[int] = None

    @field_validator("numerator", "denominator")
    @classmethod
    def positive(cls, v: Optional[int], info):
        if v is not None and v <= 0:
            raise ValueError(f"{info.field_name} must be positive")
        return v

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, v):
        if isinstance(v, str) and v.upper() == "MERGE":
            return CorporateActionType.REVERSE_SPLIT
        return v


class CorporateActionRead(CorporateActionBase):
    id: int
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
