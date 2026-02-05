from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_current_user
from app.db.session import get_db
from app.models.portfolio import Portfolio
from app.models.user import User
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioUpdate
from app.routers.utils import handle_integrity_error

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=list[PortfolioRead])
def list_portfolios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Portfolio]:
    portfolios = db.execute(select(Portfolio)).scalars().all()
    return portfolios


@router.post("", response_model=PortfolioRead, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    payload: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Portfolio:
    portfolio = Portfolio(**payload.model_dump())
    db.add(portfolio)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "Portfolio")
    db.refresh(portfolio)
    return portfolio


@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return portfolio


@router.put("/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio(
    portfolio_id: int,
    payload: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(portfolio, field, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "Portfolio")
    db.refresh(portfolio)
    return portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    db.delete(portfolio)
    db.commit()
    return None
