import asyncio
from fastapi import WebSocket

class PriceEngine:
    def __init__(self):
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
                await self.broadcast({})
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                self.is_running = False
                break
            except Exception as e:
                # continue
                await asyncio.sleep(1)

price_engine = PriceEngine()
