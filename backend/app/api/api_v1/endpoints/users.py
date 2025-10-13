"""
User management endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.deps import get_current_active_superuser, get_current_active_user
from app.db.crud.user import user as crud_user
from app.db.database import get_db
from app.schemas.user import UserInDB, UserPublic

router = APIRouter()


@router.get("/", response_model=List[UserPublic])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_superuser),
) -> List[UserPublic]:
    """
    Retrieve users (superuser only)
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return [UserPublic.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserPublic)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserPublic:
    """
    Get a specific user by ID
    """
    user = crud_user.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Users can only see their own profile unless they're superuser
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return UserPublic.model_validate(user)
