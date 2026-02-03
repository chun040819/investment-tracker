from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.report import PositionOut, PnLSummaryOut
from app.services.position_service import get_positions
from app.services.pnl_service import compute_pnl_summary

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/positions", response_model=list[PositionOut])
def positions_report(
    portfolio_id: int = Query(...),
    as_of: date | None = Query(default=None),
    in_base_currency: bool = Query(default=False, description="Convert values to portfolio base currency when possible"),
    db: Session = Depends(get_db),
) -> list[PositionOut]:
    return [PositionOut.model_validate(p) for p in get_positions(db, portfolio_id, as_of, in_base_currency=in_base_currency)]


@router.get("/pnl/summary", response_model=PnLSummaryOut)
def pnl_summary(
    portfolio_id: int = Query(...),
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    as_of: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> PnLSummaryOut:
    if from_date > to_date:
        raise HTTPException(status_code=400, detail="from must be on or before to")
    data = compute_pnl_summary(db, portfolio_id, from_date, to_date, as_of)
    return PnLSummaryOut.model_validate(data)
