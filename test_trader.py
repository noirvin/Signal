from predictor import Predictor
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_finance import candlestick_ohlc
from bot import Bot
from datetime import datetime
import matplotlib.ticker as mpticker
import Bot from bot

class Test_Trader:

    def __init__():


        self.bot = None
        self.calls= []
        self.puts=[]
        self.p_l_day=None
        self.cash = None
        self.account_value = self.cash+self.puts[0]




test_bot = Bot('AAPL')
hist_price= test_bot.get_historical_price_data('AAPL')
print(hist_price.shape)
df = pd.DataFrame(data=hist_price['AAPL'])
df=df.reset_index()
print(df)
