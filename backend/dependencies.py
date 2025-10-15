from app.websocket.price_engine import PriceEngine
from app.services.news import NewsShockSimulator

"""
Dependency injections
"""

price_engine = PriceEngine()
news_engine = NewsShockSimulator()

def get_price_engine() -> PriceEngine:
    return price_engine

def get_news_engine() -> NewsShockSimulator:
    return news_engine