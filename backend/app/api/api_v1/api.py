"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, trading, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
