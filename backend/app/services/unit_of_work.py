from __future__ import annotations

from sqlalchemy.orm import Session


class UnitOfWork:
    """Lightweight Unit of Work wrapper around a SQLAlchemy session transaction."""

    def __init__(self, db: Session):
        self.db = db
        self._tx = None

    def __enter__(self) -> "UnitOfWork":
        self._tx = self.db.begin()
        self._tx.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool | None:
        if self._tx is None:
            return None
        return self._tx.__exit__(exc_type, exc, tb)
