import time
import asyncio

class NewsShockSimulator:
    def __init__(self):
        self.news_objects = []
        self.NEWS_TICK_DELAY = 60
    
    """
    Exponential decay formula
    """
    def calculate(self, news):
        if not news:
            return 0 
        
        now_s = time.time()
        t0_s = news["ts_release_ms"] / 1000
        halflife_s = news["halflife_s"]
        magnitude = news["magnitude"]
        eff = magnitude * 2 ** (-(now_s - t0_s)/halflife_s)
        
        return eff
    
    def get_total_eff(self):
        total_eff = 0 # 0 is the baseline
        for news_object in self.news_objects:
            total_eff += self.calculate(news_object)
        return total_eff

    def add_news_ad_hoc(self, news_object):
        self.news_objects.append(news_object)
    
    async def add_news_on_tick(self):
        self.is_running = True
        while self.is_running:
            try:
                news = None # replace with DB query
                self.add_news_ad_hoc(news)
                await asyncio.sleep(self.NEWS_TICK_DELAY)
            except asyncio.CancelledError:
                self.is_running = False
                break
            except Exception as e:
                # continue
                await asyncio.sleep(1)
    
    

    