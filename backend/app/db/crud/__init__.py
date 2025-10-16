"""
CRUD operations for database models
"""

from .base import CRUDBase
from .user import CRUDUser

__all__ = [
    "CRUDBase",
    "CRUDUser",
]
