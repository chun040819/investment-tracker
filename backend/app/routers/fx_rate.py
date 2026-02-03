from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.fx_rate import FXRate
from app.schemas.fx_rate import FXRateCreate, FXRateRead, FXRateUpdate
from app.routers.utils import handle_integrity_error

router = APIRouter(prefix="/fx-rates", tags=["fx-rates"])


@router.get("", response_model=list[FXRateRead])
def list_fx_rates(
    from_currency: str | None = Query(default=None),
    to_currency: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[FXRate]:
    stmt = select(FXRate)
    if from_currency:
        stmt = stmt.where(FXRate.from_currency == from_currency)
    if to_currency:
        stmt = stmt.where(FXRate.to_currency == to_currency)
    stmt = stmt.order_by(FXRate.date.desc(), FXRate.id.desc())
    return db.execute(stmt).scalars().all()


@router.post("", response_model=FXRateRead, status_code=status.HTTP_201_CREATED)
def create_fx_rate(payload: FXRateCreate, db: Session = Depends(get_db)) -> FXRate:
    fx = FXRate(**payload.model_dump())
    db.add(fx)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "FXRate")
    db.refresh(fx)
    return fx


@router.get("/{fx_id}", response_model=FXRateRead)
def get_fx_rate(fx_id: int, db: Session = Depends(get_db)) -> FXRate:
    fx = db.get(FXRate, fx_id)
    if not fx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FX rate not found")
    return fx


@router.put("/{fx_id}", response_model=FXRateRead)
def update_fx_rate(fx_id: int, payload: FXRateUpdate, db: Session = Depends(get_db)) -> FXRate:
    fx = db.get(FXRate, fx_id)
    if not fx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FX rate not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(fx, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "FXRate")
    db.refresh(fx)
    return fx


@router.delete("/{fx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fx_rate(fx_id: int, db: Session = Depends(get_db)) -> None:
    fx = db.get(FXRate, fx_id)
    if not fx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FX rate not found")
    db.delete(fx)
    db.commit()
    return None
