from fastapi import APIRouter, Depends

from app.core.security import fetch_current_user
from app.db.models import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/dashboard")
def dashboard(current_user: User = Depends(fetch_current_user)):
    return {"message": f"Welcome {current_user.email}"}
