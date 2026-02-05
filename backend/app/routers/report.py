from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.report import PositionOut, PnLSummaryOut
from app.services.position_service import get_positions
from app.services.pnl_service import compute_pnl_summary
from app.services.cache import cache_get, cache_set
from app.core.config import settings

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/positions", response_model=list[PositionOut])
def positions_report(
    portfolio_id: int = Query(...),
    as_of: date | None = Query(default=None),
    in_base_currency: bool = Query(default=False, description="Convert values to portfolio base currency when possible"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[PositionOut]:
    cache_key = f"cache:portfolio:{portfolio_id}:positions:{as_of}:{int(in_base_currency)}"
    cached = cache_get(cache_key)
    if cached is not None:
        return [PositionOut.model_validate(p) for p in cached]

    results = [PositionOut.model_validate(p) for p in get_positions(db, portfolio_id, as_of, in_base_currency=in_base_currency)]
    cache_set(
        cache_key,
        [r.model_dump(mode="json") for r in results],
        ttl_seconds=settings.cache_ttl_seconds,
    )
    return results


@router.get("/pnl/summary", response_model=PnLSummaryOut)
def pnl_summary(
    portfolio_id: int = Query(...),
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    as_of: date | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PnLSummaryOut:
    if from_date > to_date:
        raise HTTPException(status_code=400, detail="from must be on or before to")
    cache_key = f"cache:portfolio:{portfolio_id}:pnl_summary:{from_date}:{to_date}:{as_of}"
    cached = cache_get(cache_key)
    if cached is not None:
        return PnLSummaryOut.model_validate(cached)

    data = compute_pnl_summary(db, portfolio_id, from_date, to_date, as_of)
    result = PnLSummaryOut.model_validate(data)
    cache_set(cache_key, result.model_dump(mode="json"), ttl_seconds=settings.cache_ttl_seconds)
    return result
