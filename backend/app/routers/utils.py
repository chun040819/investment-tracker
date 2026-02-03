from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def handle_integrity_error(exc: IntegrityError, entity: str) -> None:
    """Translate DB integrity errors (e.g., unique constraint) into HTTP 409."""
    detail = f"{entity} already exists or violates a constraint"
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail) from exc
