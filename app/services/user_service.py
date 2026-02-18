from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User


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

    if not user:
        return None

    if not verify_password(password, str(user.password_hash)):
        return None

    access_token = create_access_token(data={"sub": str(user.id)})

    return access_token
