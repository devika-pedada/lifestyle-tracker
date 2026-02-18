from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth_schema import RegisterResponse
from app.schemas.user_schema import UserRegisterRequest
from app.services.user_service import create_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(db=db, name=request.name, email=request.email, password=request.password)

        return {"message": "User created successfully", "user_id": user.id}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
