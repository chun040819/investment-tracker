from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User

DEFAULT_USER_EMAIL = "admin@example.com"
DEFAULT_USER_PASSWORD = "dummy-password"


def get_current_user(db: Session = Depends(get_db)) -> User:
    # Ensure single-user mode works even before migrations create the table.
    User.__table__.create(bind=db.get_bind(), checkfirst=True)

    user = db.execute(select(User).where(User.email == DEFAULT_USER_EMAIL)).scalars().first()
    if user:
        return user

    user = User(email=DEFAULT_USER_EMAIL, hashed_password=DEFAULT_USER_PASSWORD)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        user = db.execute(select(User).where(User.email == DEFAULT_USER_EMAIL)).scalars().first()
        if user is None:
            raise
        return user

    db.refresh(user)
    return user
