"""
Trading Simulator FastAPI Application
Main entry point for the trading simulator backend
"""

import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.database import engine
from app.models import models
from app.websocket.price_engine import price_engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trading Simulator API",
    description="A web-based stock trading simulator for live competitions",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Trading Simulator API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/version")
async def version_check():
    return {"version": "1.0.0"}


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(price_engine.run())


@app.websocket("/ws/market")
async def websocket_market(websocket: WebSocket):
    await price_engine.connect(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except Exception as e:
        pass
    finally:
        price_engine.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
