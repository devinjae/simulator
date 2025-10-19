import random
import json

class LiquidityBot:
    def __init__(self, instrument_id, mid_price, inventory):
        self.instrument_id = instrument_id
        self.mid_price = mid_price 
        self.inventory = inventory 

        self.base_spread = 0.1 
        self.stress_coefficient = random.uniform(0.05, 0.15) # based on dc discussion
        self.inventory_coefficient = random.uniform(0.005, 0.05) # based on dc discussion
        self.quote_noise_sigma = 0.05 

    def compute_spread(self, drift_term):
        """
        spread_i = s0 + k * |Φ_i(t)| + γ * |Q_i| + η
        """
        eta = random.gauss(0, self.quote_noise_sigma)
        spread = (
            self.base_spread
            + self.stress_coefficient * abs(drift_term)
            + self.inventory_coefficient * abs(self.inventory)
            + eta
        )
        return spread

    def compute_quotes(self, spread):
        """
        Places symmetric quotes:
        bid = M_i * (1 - spread_i/2)
        ask = M_i * (1 + spread_i/2)
        """
        bid = self.mid_price * (1 - spread / 2)
        ask = self.mid_price * (1 + spread / 2)
        return bid, ask

    def depth_curve(self, level):
        """
        depth_curve = max(50 - 10 * level, 10)
        """
        return max(50 - 10 * level, 10)

    def generate_order_book(self, drift_term, levels=3):
        spread = self.compute_spread(drift_term)
        bid, ask = self.compute_quotes(spread)

        bids = []
        asks = []

        for lvl in range(levels):
            depth = self.depth_curve(lvl)
            bid_price = round(bid - lvl * spread, 2)
            ask_price = round(ask + lvl * spread, 2)

            bids.append([bid_price, depth])
            asks.append([ask_price, depth])

        book_snapshot = {
            "type": "book_snapshot",
            "instrumentId": self.instrument_id,
            "bids": bids,
            "asks": asks
        }

        return book_snapshot

# For testing only
if __name__ == "__main__":
    bot = LiquidityBot(instrument_id="AAPL", mid_price=180.0, inventory=random.randint(-5, 5))
    drift_term = random.uniform(-1, 1)
    snapshot = bot.generate_order_book(drift_term)
    print(json.dumps(snapshot, indent=2))
