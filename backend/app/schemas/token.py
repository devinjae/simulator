"""
Token-related schemas
"""

from pydantic import BaseModel

from .user import UserPublic


class Token(BaseModel):
    """Token response schema"""

    access_token: str
    token_type: str
    expires_in: int  # seconds
    user: UserPublic


class TokenData(BaseModel):
    """Token data schema"""

    username: str | None = None
