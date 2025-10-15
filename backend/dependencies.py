from app.websocket.price_engine import PriceEngine
from app.services.news import NewsShockSimulator

"""
For dependency injections, these are all singletons
"""

news_engine = NewsShockSimulator()
price_engine = PriceEngine(news_engine=news_engine)

def get_price_engine() -> PriceEngine:
    return price_engine

def get_news_engine() -> NewsShockSimulator:
    return news_engine