from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_current_user
from app.db.session import get_db
from app.models.corporate_action import CorporateAction
from app.models.user import User
from app.schemas.corporate_action import (
    CorporateActionCreate,
    CorporateActionRead,
    CorporateActionUpdate,
)
from app.routers.utils import handle_integrity_error

router = APIRouter(prefix="/corporate-actions", tags=["corporate-actions"])


@router.get("", response_model=list[CorporateActionRead])
def list_actions(
    asset_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CorporateAction]:
    stmt = select(CorporateAction)
    if asset_id is not None:
        stmt = stmt.where(CorporateAction.asset_id == asset_id)
    stmt = stmt.order_by(CorporateAction.date, CorporateAction.id)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=CorporateActionRead, status_code=status.HTTP_201_CREATED)
def create_action(
    payload: CorporateActionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CorporateAction:
    action = CorporateAction(**payload.model_dump())
    db.add(action)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "CorporateAction")
    db.refresh(action)
    return action


@router.get("/{action_id}", response_model=CorporateActionRead)
def get_action(
    action_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CorporateAction:
    action = db.get(CorporateAction, action_id)
    if not action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corporate action not found")
    return action


@router.put("/{action_id}", response_model=CorporateActionRead)
def update_action(
    action_id: int,
    payload: CorporateActionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CorporateAction:
    action = db.get(CorporateAction, action_id)
    if not action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corporate action not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(action, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        handle_integrity_error(exc, "CorporateAction")
    db.refresh(action)
    return action


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action(
    action_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    action = db.get(CorporateAction, action_id)
    if not action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Corporate action not found")
    db.delete(action)
    db.commit()
    return None
