import asyncio
from fastapi import WebSocket
from app.services.gbm import GeometricBrownianMotionAssetSimulator


class PriceEngine:
    def __init__(self):
        # TODO: convert to map, should be ticker -> connections
        # also add another map ticker -> gbm simulator
        self.active_connections = set()
        self.is_running = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to connection: {e}")
                self.disconnect(connection)

    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                gbmas = GeometricBrownianMotionAssetSimulator(100, 0.05, 0.5, 1/252)
                await self.broadcast(gbmas())
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                self.is_running = False
                break
            except Exception as e:
                # continue
                await asyncio.sleep(1)


price_engine = PriceEngine()
