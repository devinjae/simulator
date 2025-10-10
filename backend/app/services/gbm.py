import numpy as np

class GeometricBrownianMotionAssetSimulator:
    def __init__(self, initial_price, mu, sigma):
        # queried from UBC TG DB
        self.initial_price = initial_price
        self.mu = mu
        self.sigma = sigma
        
        # TODO: store previous prices 
    
    @staticmethod
    def generate_e():
        return np.random.normal(0, 1) # random sampling E
    
    def calculate(self):
        # TODO: calculate next price using GBM formula
        pass
    
    def __call__(self):
        return self.calculate()