#!/usr/bin/env python3
"""
Script to create a user (admin or regular)
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv(backend_dir / ".env")

from sqlmodel import Session

from app.db.crud.user import user as user_crud
from app.db.database import engine
from app.schemas.user import UserCreate


def create_user(username: str, email: str, password: str, is_superuser: bool = False):
    """Create a user with specified credentials"""

    with Session(engine) as db:
        # Check if user already exists
        existing_user = user_crud.get_by_username(db, username=username)
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False

        # Check if email is already taken
        if email and user_crud.get_by_email(db, email=email):
            print(f"❌ Email '{email}' is already registered!")
            return False

        # Create user
        try:
            user_create = UserCreate(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_superuser=is_superuser,
            )

            user = user_crud.create(db, obj_in=user_create)

            user_type = "Admin" if is_superuser else "Regular"
            print(f"✅ {user_type} user created successfully!")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   User ID: {user.id}")
            print(f"   Is Superuser: {user.is_superuser}")
            print(f"   Is Active: {user.is_active}")

            return True

        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return False


def main():
    """Main function with command line arguments"""
    if len(sys.argv) < 4:
        print("Usage: python create_user.py <username> <email> <password> [--admin]")
        print()
        print("Examples:")
        print("  python create_user.py john john@example.com mypassword")
        print("  python create_user.py admin admin@example.com adminpass --admin")
        sys.exit(1)

    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    is_superuser = "--admin" in sys.argv

    print(f"🚀 Creating {'admin' if is_superuser else 'regular'} user...")
    print()

    success = create_user(username, email, password, is_superuser)

    if success:
        print()
        print("🎉 User created successfully!")
    else:
        print()
        print("💥 Failed to create user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
