from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import fetch_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterResponse
from app.schemas.user import UserRegisterRequest, UserResponse
from app.services.user import authenticate_user, create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(db=db, name=request.name, email=request.email, password=request.password)

        return {"message": "User created successfully", "user_id": user.id}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


def _handle_login(email: str, password: str, db: Session):
    tokens = authenticate_user(db=db, email=email, password=password)

    if not tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return tokens


@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    return _handle_login(email=request.email, password=request.password, db=db)


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    tokens = _handle_login(email=form_data.username, password=form_data.password, db=db)  # OAuth uses username field

    return {"access_token": tokens["access_token"], "token_type": "bearer"}


@router.get("/current_user", response_model=UserResponse)
def get_current_user(current_user: User = Depends(fetch_current_user)):
    return current_user
