"""
Authentication endpoints
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.config import settings
from app.core.deps import get_current_active_user
from app.core.security import create_access_token
from app.db.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserInDB, UserPublic
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        user=UserPublic.model_validate(user),
    )


@router.post("/register", response_model=UserPublic)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)) -> UserPublic:
    """
    Register a new user
    """
    try:
        user = AuthService.create_user(db, user_create)
        return UserPublic.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=UserPublic)
def read_user_me(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserPublic:
    """
    Get current user information
    """
    return UserPublic.model_validate(current_user)


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: UserInDB = Depends(get_current_active_user)) -> UserPublic:
    """
    Test access token
    """
    return UserPublic.model_validate(current_user)
