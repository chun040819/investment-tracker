from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.position_snapshot import PositionSnapshot
from app.services.position_service import get_positions


def create_daily_snapshots(
    db: Session,
    portfolio_id: int,
    snapshot_date: date | None = None,
    replace_existing: bool = True,
) -> list[PositionSnapshot]:
    """
    Materialize holdings for a portfolio on a given date.

    The calculation deliberately bypasses existing snapshots to avoid compounding
    drift. Use this from a daily job or after large backfills.
    """
    if snapshot_date is None:
        snapshot_date = datetime.now(timezone.utc).date()

    positions = get_positions(
        db,
        portfolio_id=portfolio_id,
        as_of=snapshot_date,
        in_base_currency=False,
        use_snapshots=False,
        include_realized=True,
    )

    if replace_existing:
        db.execute(
            delete(PositionSnapshot).where(
                PositionSnapshot.portfolio_id == portfolio_id,
                PositionSnapshot.snapshot_date == snapshot_date,
            )
        )

    snapshots: list[PositionSnapshot] = []
    for pos in positions:
        snap = PositionSnapshot(
            portfolio_id=portfolio_id,
            asset_id=pos["asset_id"],
            snapshot_date=snapshot_date,
            shares=pos["shares_held"],
            cost_basis=pos["cost_basis"],
            realized_pnl=pos.get("realized_pnl", Decimal("0")),
        )
        db.add(snap)
        snapshots.append(snap)

    db.commit()
    for snap in snapshots:
        db.refresh(snap)

    return snapshots
