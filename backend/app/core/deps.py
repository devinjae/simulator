"""
Dependencies for authentication and authorization
"""

import logging
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.config import settings
from app.core.security import verify_token
from app.db.crud.user import user as user_crud
from app.db.database import get_db
from app.schemas.user import UserInDB

# HTTP Bearer token scheme
security = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserInDB:
    """
    Get the current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token
    username = verify_token(credentials.credentials)
    if username is None:
        raise credentials_exception

    # Get user from database
    user = user_crud.get_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return UserInDB.model_validate(user)


def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    """
    Get the current active user (must be authenticated and active)
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    """
    Get the current active superuser (must be authenticated, active, and superuser)
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


# Optional authentication dependency (returns None if not authenticated)
def get_current_user_optional(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[UserInDB]:
    """
    Get the current user if authenticated, otherwise return None
    """
    if credentials is None:
        return None

    username = verify_token(credentials.credentials)
    if username is None:
        return None

    user = user_crud.get_by_username(db, username=username)
    if user is None:
        return None

    return UserInDB.model_validate(user)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
