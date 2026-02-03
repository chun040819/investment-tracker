from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.routers.utils import handle_integrity_error
from app.models.tag import Tag

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=list[AssetRead])
def list_assets(symbol: str | None = Query(default=None, description="Filter by symbol"), db: Session = Depends(get_db)) -> list[Asset]:
    stmt = select(Asset)
    if symbol:
        stmt = stmt.where(Asset.symbol == symbol)
    assets = db.execute(stmt).scalars().all()
    return assets


def _upsert_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    tags: list[Tag] = []
    for name in tag_names:
        existing = db.execute(select(Tag).where(Tag.name == name)).scalars().first()
        if existing:
            tags.append(existing)
        else:
            new_tag = Tag(name=name)
            db.add(new_tag)
            tags.append(new_tag)
    return tags


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)) -> Asset:
    data = payload.model_dump()
    tag_names = data.pop("tags", None)
    asset = Asset(**data)
    if tag_names:
        asset.tags = _upsert_tags(db, tag_names)
    db.add(asset)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "Asset")
    db.refresh(asset)
    return asset


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(asset_id: int, db: Session = Depends(get_db)) -> Asset:
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetRead)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)) -> Asset:
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    data = payload.model_dump(exclude_unset=True)
    tag_names = data.pop("tags", None)
    for field, value in data.items():
        setattr(asset, field, value)
    if tag_names is not None:
        asset.tags = _upsert_tags(db, tag_names)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "Asset")
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: int, db: Session = Depends(get_db)) -> None:
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    db.delete(asset)
    db.commit()
    return None
