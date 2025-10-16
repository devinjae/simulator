import asyncio
from fastapi import WebSocket
from app.services.gbm import GeometricBrownianMotionAssetSimulator


class PriceEngine:
    def __init__(self):
        # TODO: convert to map, should be ticker -> connections
        # also add another map ticker -> gbm simulator
        self.active_connections = set()
        self.is_running = False
        self.tickers = [
            {
                "ticker": "AAPL",
                "current_price": 180.0,
                "mu": 0.07,
                "sigma": 0.25
            },
            {
                "ticker": "TSLA",
                "current_price": 250.0,
                "mu": 0.10,
                "sigma": 0.40
            },
            {
                "ticker": "GOOG",
                "current_price": 340.0,
                "mu": 0.06,
                "sigma": 0.22
            },
            {
                "ticker": "AMZN",
                "current_price": 100.0,
                "mu": 0.08,
                "sigma": 0.30
            }
        ]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message):
        # None connected
        if not self.active_connections:
            return

        coros = []
        for connection in list(self.active_connections):
            coros.append(self._safe_send(connection, message))

        # Run all concurrently instead of sequentially
        await asyncio.gather(*coros, return_exceptions=True)

    async def _safe_send(self, connection: WebSocket, message):
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error broadcasting to connection: {e}")
            self.disconnect(connection)

    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                self.gbmas_instances = {
                    ticker["ticker"]:
                        GeometricBrownianMotionAssetSimulator(
                            ticker["current_price"], ticker["mu"], ticker["sigma"], 1/252)
                        for ticker in self.tickers
                }
                await self.broadcast({
                    ticker: gbmas() for ticker, gbmas in self.gbmas_instances.items()
                })
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                self.is_running = False
                break
            except Exception as e:
                # continue
                await asyncio.sleep(1)
