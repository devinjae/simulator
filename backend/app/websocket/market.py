from fastapi import WebSocket, APIRouter
from .price_engine import price_engine

websocket_router = APIRouter()

@websocket_router.websocket("/ws/market")
async def websocket_market(websocket: WebSocket):
    await price_engine.connect(websocket)
    try:
        await websocket.wait_closed() # keep connection alive
    finally:
        price_engine.disconnect(websocket)
