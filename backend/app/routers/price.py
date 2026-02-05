from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_current_user
from app.db.session import get_db
from app.models.asset import Asset
from app.models.price_history import PriceHistory
from app.models.user import User
from app.schemas.price import PricePoint, PriceUpdateResult
from app.services.pricing import fetch_daily_close
from app.services.cache import cache_get, cache_set, cache_delete
from app.core.config import settings
from app.routers.utils import handle_integrity_error

router = APIRouter(prefix="/prices", tags=["prices"])


@router.post("/update", response_model=PriceUpdateResult)
def update_prices(
    asset_id: int = Query(...),
    start: date = Query(...),
    end: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PriceUpdateResult:
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    try:
        closes = fetch_daily_close(asset.symbol, start, end)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    # Fetch existing records for upsert comparison
    existing_stmt = (
        select(PriceHistory).where(
            and_(
                PriceHistory.asset_id == asset_id,
                PriceHistory.date >= start,
                PriceHistory.date <= end,
            )
        )
    )
    existing = {ph.date: ph for ph in db.execute(existing_stmt).scalars().all()}

    inserted = 0
    updated = 0

    for price_date, close in closes:
        if price_date in existing:
            ph = existing[price_date]
            if ph.close != close or ph.currency != asset.currency:
                ph.close = close
                ph.currency = asset.currency
                updated += 1
        else:
            ph = PriceHistory(
                asset_id=asset_id,
                date=price_date,
                close=close,
                currency=asset.currency,
            )
            db.add(ph)
            inserted += 1

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "PriceHistory")

    cache_delete(f"cache:price:latest:{asset_id}")
    return PriceUpdateResult(inserted=inserted, updated=updated)


@router.get("/latest", response_model=PricePoint)
def latest_price(
    asset_id: int = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PricePoint:
    cache_key = f"cache:price:latest:{asset_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        return PricePoint.model_validate(cached)

    stmt = (
        select(PriceHistory)
        .where(PriceHistory.asset_id == asset_id)
        .order_by(PriceHistory.date.desc())
        .limit(1)
    )
    ph = db.execute(stmt).scalars().first()
    if not ph:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No price data found")
    result = PricePoint.model_validate(ph)
    cache_set(cache_key, result.model_dump(mode="json"), ttl_seconds=settings.cache_ttl_seconds)
    return result
