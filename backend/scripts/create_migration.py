#!/usr/bin/env python3
"""
Script to create database migration for users table
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Create migration for users table"""
    backend_dir = Path(__file__).parent.parent

    try:
        # Change to backend directory
        subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                "revision",
                "--autogenerate",
                "-m",
                "add_users_table",
            ],
            cwd=backend_dir,
            check=True,
        )
        print("✅ Migration created successfully!")
        print("📝 Review the generated migration file before applying it.")
        print("🚀 Run 'alembic upgrade head' to apply the migration.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating migration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
