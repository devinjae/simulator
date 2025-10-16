"""
Authentication service for user management
"""

from typing import Optional

from sqlmodel import Session

from app.db.crud.user import user as user_crud
from app.schemas.user import UserCreate, UserInDB, UserUpdate


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[UserInDB]:
        """Get user by username"""
        user = user_crud.get_by_username(db, username=username)
        if user:
            return UserInDB.model_validate(user)
        return None

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        user = user_crud.get_by_email(db, email=email)
        if user:
            return UserInDB.model_validate(user)
        return None

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserInDB]:
        """Get user by ID"""
        user = user_crud.get(db, user_id)
        if user:
            return UserInDB.model_validate(user)
        return None

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> UserInDB:
        """Create a new user"""
        try:
            user = user_crud.create(db, obj_in=user_create)
            return UserInDB.model_validate(user)
        except ValueError as e:
            raise e

    @staticmethod
    def authenticate_user(
        db: Session, username: str, password: str
    ) -> Optional[UserInDB]:
        """Authenticate a user with username and password"""
        user = user_crud.authenticate(db, username=username, password=password)
        if user:
            return UserInDB.model_validate(user)
        return None

    @staticmethod
    def update_user(
        db: Session, user_id: int, user_update: UserUpdate
    ) -> Optional[UserInDB]:
        """Update a user"""
        db_user = user_crud.get(db, user_id)
        if not db_user:
            return None

        updated_user = user_crud.update(db, db_obj=db_user, obj_in=user_update)
        return UserInDB.model_validate(updated_user)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        user = user_crud.remove(db, id=user_id)
        return user is not None
