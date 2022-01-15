import numpy as np
import pandas as pd

class Company:

    def __init__(self,symbol):

        self.symbol=symbol
        self.minute_df = None
        self.daily_df =pd.DataFrame()
        self.average_trade_volume=[]
        self.trade_volume=0
        self.total_trades_per_minute=0
        self.data_per_minute= np.array([])
        self.prices=[]
        self.low=None
        self.high=0
        self.open= 0
        self.close=0
        self.timestamps=None
        self.curr_avg_trade_volumes=[]
        self.curr_avg_volume=None
        self.daily_avg_volume=None
        self.predictor=None
        self.start_time=None
        self.thirty_day_avg_vol = 0
        self.thirty_day_df = pd.DataFrame()
        self.test_lines = {}
        self.signal=None
        self.in_position_calls=False
        self.in_position_puts=False
        self.calls_bought_at = 0
        self.puts_bought_at = 0
        self.share_numbers = None
        self.profit_loss=None
        self.initial_investment = None
        # self.companies['TSLA'].prices[len(self.companies['TSLA'].prices)-1]
