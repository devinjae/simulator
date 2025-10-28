
class UserState:
    """
    Example of an order (for reference):
    {
        "price": 101.5,
        "quantity": 5,
        "ticker": "AAPL",
        "user_id": "u1",
        "side": "buy"
    }
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.cash = 0
        self.unfulfilled_trades = []
        self.buys = []
        self.total_shares = 0
        self.prev_avg_price = 0
        self.realized_pnl = 0

    # adds order that is closed and so we call get_avg_price here
    def add_buy(self, order):
        self.buys.append(order)
        self.realized_pnl = self.get_avg_price(order["price"], order["quantity"])

    # TODO: implement remove shares FIFO
    def remove_buy(self):
        pass

    def add_unfulfilled_trade(self, order):
        self.unfulfilled_trades.append(order)

    def get_avg_price(self, order_price, order_quantity) -> float:
        prev_quantity = self.total_shares
        self.total_shares += order_quantity

        # should we check for negatives as well here?
        if self.total_shares == 0:
            return 0

        avg_price = (
            (self.prev_avg_price * prev_quantity) +
            (order_price * order_quantity)
        ) / self.total_shares

        self.prev_avg_price = avg_price

        return avg_price

    # then this would be a separate thing right?
    # TODO: implement pnl calculation
    def calculate_realized_pnl(self):
        self.realized_pnl = 0
