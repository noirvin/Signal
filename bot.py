from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from alpaca_trade_api.stream import Stream
from datetime import datetime
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from predictor import Predictor
from sklearn.cluster import KMeans
import pendulum
import pytz




 # pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
 #                   columns=['a', 'b', 'c'])


api = REST(key_id='AK6XD1EIN49YAJYBTSO8',secret_key='Wvdxl7a7oDlN0MBE7zkDzbg3SqHachg1cyyQn39i', api_version='v2')
stream = Stream(key_id='AK6XD1EIN49YAJYBTSO8',
                secret_key='Wvdxl7a7oDlN0MBE7zkDzbg3SqHachg1cyyQn39i',
                data_feed='sip')
trade_volume=[]


class Bot:

    def __init__(self, stocks_to_watch):

        self.stocks_to_watch= stocks_to_watch
        self.initial_start = datetime.now()
        self.curr_avg_trade_volumes=[]
        self.curr_avg_volume = None
        self.daily_avg_volume = None
        self.trade_volume=0
        self.total_trades_per_minute=0
        self.data_per_minute= np.array([])
        self.prices=[]
        self.low=0
        self.high=0
        self.open= 0
        self.close=0
        self.start_time = None
        self.reset_val_cond=False
        self.predictor=None
        self.timestamps=None
        self.df=None
        self.initial_data_collection=False


    def get_historical_price_data(self, company):
        now = pd.Timestamp.now(tz='US/Pacific').floor('1min')
        today = now.strftime('%Y-%m-%d')
        tomorrow = (now + pd.Timedelta('1day')).strftime('%Y-%m-%d')
        bar = api.get_barset([company], 'minute', start=today, end=tomorrow).df
        return bar


    def signal_breakout(self,resistance,support,price):
        if price<support:
            return 's'
        if price>resistance:
            return 'r'

    def signal_buy_sell(self,price,resistance,support,curr_avg_volume,daily_avg_volume):

        if self.signal_breakout(resistance,support,price)=='r':
            if curr_avg_volume>=daily_avg_volume*0.6:
                return 'buy'
        if self.signal_breakout(resistance,support,price)=='s':
            if curr_avg_volume>=daily_avg_volume*0.3:
                return 'sell'
        else:
            return None



    def get_bars(self,t):
        if self.start_time is None and self.reset_val_cond==True:
            self.reset_val_cond=False

        if self.start_time is None:
            self.start_time = datetime.now()
            # np.append(self.timestamps,get_time(t.timestamp))
            self.open=t.price
            self.low=t.price
            self.high=t.price


        if self.initial_data_collection == True:
            if self.predictor == None:
                self.predictor= Predictor(self.df)
                lows = pd.DataFrame(data=self.predictor.df, index=self.predictor.df.index, columns=["Low"])
                highs = pd.DataFrame(data=self.predictor.df, index=self.predictor.df.index, columns=["High"])

                self.predictor.predict_resistance(highs)
                self.predictor.predict_support(lows)


                print("Resistance: ")
                print(self.predictor.resistances)
                print("Supports: ")
                print(self.predictor.supports)
            signal = self.signal_buy_sell(t.price,max(self.predictor.resistances),min(self.predictor.supports),self.curr_avg_volume,self.daily_avg_volume)
            if signal is not None:
                print(signal)

        if  datetime.now().minute>=(self.start_time.minute+1):
            print("got to here")
            self.timestamps=t.timestamp
            self.close=t.price
            self.data_per_minute= np.append(self.data_per_minute,np.array([self.timestamps,self.open,self.close,self.high,self.low]))
            self.curr_avg_volume = self.trade_volume/self.total_trades_per_minute
            self.curr_avg_trade_volumes.append(self.curr_avg_volume)

            self.reset_values()

            self.reset_val_cond=True
        if datetime.now().minute>=(self.initial_start.minute+15):
            self.initial_data_collection=True
            self.daily_avg_volume=(sum(self.curr_avg_trade_volumes)/15)
            print("got to here too")
            self.df = pd.DataFrame(self.data_per_minute.reshape(15,5), columns=['Timestamp','Open','Close','High','Low'])

            self.initial_start = datetime.now()
            self.reset_values()

        if self.reset_val_cond==False:
            if t.price>self.high:
                self.high = t.price
            if t.price<self.low:
                self.low=t.price
            self.total_trades_per_minute+=1
            if t.size!=0:

                self.trade_volume+=t.size

    def reset_values(self):
        self.start_time=None
        self.close=0
        self.total_trades_per_minute=0
        self.trade_volume=0


    def get_live_price_data(self,company):
        # for company in companies:
        stream.subscribe_trades(self.trade_callback,company)
        stream.run()
    async def trade_callback(self,t):

        # self.trade_volume.append(t.size)
        # print(self.trade_volume)
        # print(t)
        self.get_bars(t)

        # print(t.size)
        # print(test_dic[0]['size'])


# test_bot = Bot('AAPL')
# test_bot.get_live_price_data('AAPL')
# dt='1639151967849843839'
# dt = datetime.fromtimestamp(int(dt))
pst= pytz.timezone('US/Pacific')
def get_time(unix_epoch_time):
    my_datetime = str(pd.to_datetime(unix_epoch_time, unit='ns', utc=True))

    time= datetime((int(my_datetime[0:4])),(int(my_datetime[5:7])),(int(my_datetime[8:10])),(int(my_datetime[11:13])),(int(my_datetime[14:16])),(int(my_datetime[17:19])))

    return time.time


test_bot = Bot('AAPL')
# print(test_bot.get_historical_price_data('AAPL'))
test_bot.get_live_price_data('AAPL')
