from unittest import TestCase
from app.services.order_book import OrderBook

class TestOrderBook(TestCase):
    def setUp(self):
        self.order_book = OrderBook()
    
    def test_order_insertion_start(self):
        pass

    def test_order_insertion_end(self):
        pass
    
    def test_order_insertion_middle(self):
        pass

    def test_order_matching_partial(self):
        pass
    
    def test_order_matching_full(self):
        pass
    
    def test_order_matching_no_match(self):
        pass