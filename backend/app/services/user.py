
class UserState:

    def __init__(self, user_id):
        self.user_id = user_id
        self.cash = 0
        self.unfulfilled_trades = []
        self.buys = []
        self.realized_pnl = 0
        self.total_shares = 0

    # adds order that is closed and so we call get_avg_price here
    def add_buy(self, ticker, order_price, order_quantity):
        self.buys.append({
            "ticker": ticker,
            "order_price": order_price,
            "order_quantity": order_quantity
        })
        self.realized_pnl = self.get_avg_price(order_price, order_quantity)

    def add_unfulfilled_trade(self, ticker, order_price, order_quantity):
        self.add_unfulfilled_trade.append({
            "ticker": ticker,
            "order_price": order_price,
            "order_quantity": order_quantity
        })

    def get_avg_price(self, order_price, order_quantity) -> float:
        prev_quantity = self.total_shares
        self.total_shares += order_quantity
        avg_price = ((self.realized_pnl * prev_quantity) + order_price) / self.total_shares
        return avg_price
