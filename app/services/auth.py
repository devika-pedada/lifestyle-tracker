from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.core.security import create_access_token, create_refresh_token, get_refresh_token_expiry
from app.db.models import RefreshToken

logger = get_logger(__name__)


def refresh_access_token(db: Session, refresh_token_value: str):
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token_value, RefreshToken.is_revoked.is_(False))
        .first()
    )

    if not token:
        logger.warning("Invalid refresh token attempt")
        return None

    if token.expires_at < datetime.now(timezone.utc):
        logger.warning("Expired refresh token used")
        return None

    user = token.user
    # rotate token
    token.is_revoked = True

    new_refresh_value = create_refresh_token()
    new_refresh = RefreshToken(token=new_refresh_value, user_id=user.id, expires_at=get_refresh_token_expiry())

    db.add(new_refresh)
    db.commit()

    access_token = create_access_token(data={"sub": str(user.email)})
    logger.info(f"Refresh token rotated for user_id={user.email}")

    return {"access_token": access_token, "refresh_token": new_refresh_value}
