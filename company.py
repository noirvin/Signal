import numpy as np


class Company:

    def __init__(self,symbol):

        self.symbol=symbol
        self.average_trade_volume=[]
        self.trade_volume=0
        self.total_trades_per_minute=0
        self.data_per_minute= np.array([])
        self.prices=[]
        self.low=0
        self.high=0
        self.open= 0
        self.close=0

        
