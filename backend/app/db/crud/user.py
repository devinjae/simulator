"""
CRUD operations for User model
"""

from typing import Optional

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model"""

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Get user by username"""
        statement = select(User).where(User.username == username)
        return db.exec(statement).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user with hashed password"""
        # Check if username already exists
        if self.get_by_username(db, username=obj_in.username):
            raise ValueError("Username already registered")

        # Check if email already exists (if provided)
        if obj_in.email and self.get_by_email(db, email=obj_in.email):
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = get_password_hash(obj_in.password)

        # Create user object
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=hashed_password,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )

        # Add to database
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user with password hashing if needed"""
        update_data = obj_in.model_dump(exclude_unset=True)

        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        # Update timestamp
        from datetime import datetime

        update_data["updated_at"] = datetime.utcnow()

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        """Authenticate a user with username or email and password"""
        # Try username first
        user = self.get_by_username(db, username=username)
        # If not found, try email
        if not user:
            user = self.get_by_email(db, email=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser


# Create instance
user = CRUDUser(User)
