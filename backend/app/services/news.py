import time

class NewsShockSimulator:
    def __init__(self):
        pass
    
    """
    Exponential decay formula
    """
    def calculate(self, news):
        now_s = time.time()
        t0_s = news["ts_release_ms"] / 1000
        halflife_s = news["halflife_s"]
        magnitude = news["magnitude"]
        eff = magnitude * 2 ** (-(now_s - t0_s)/halflife_s)
        return eff