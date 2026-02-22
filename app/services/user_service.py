from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_refresh_token_expiry,
    hash_password,
    verify_password,
)
from app.db.models import RefreshToken, User

logger = get_logger(__name__)


def create_user(db: Session, name: str, email: str, password: str):
    hashed_pwd = hash_password(password)

    user = User(name=name, email=email, password_hash=hashed_pwd)

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        logger.warning(f"Login failed: user not found or invalid password - {email}")
        return None

    access_token = create_access_token(data={"sub": str(user.id)})

    refresh_token_value = create_refresh_token()

    refresh_token = RefreshToken(token=refresh_token_value, user_id=user.id, expires_at=get_refresh_token_expiry())

    db.add(refresh_token)
    db.commit()

    logger.info(f"User logged in successfully - user_id={user.id}")

    return {"access_token": access_token, "refresh_token": refresh_token_value}
