from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
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
