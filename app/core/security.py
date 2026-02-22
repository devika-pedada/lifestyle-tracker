import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.logging import get_logger

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7
SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

logger = get_logger(__name__)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token():
    return secrets.token_urlsafe(64)


def get_refresh_token_expiry():
    return datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
