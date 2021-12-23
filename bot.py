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
        self.average_trade_volume=[]
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
        self.timestamps=np.array([])
        self.df=None


    def get_historical_price_data(self, company):

        api.get_bars(company, TimeFrame.Hour, "2021-11-08", "2021-11-08", adjustment='raw').df



    def get_resup(self,price,avg_volume):

        pass

    def signal_buy(self,price,avg_volume):

        pass

    def signal_sell(self,price_data,resup):

        pass


    def get_bars(self,t):
        if self.start_time is None and self.reset_val_cond==True:
            self.reset_val_cond=False

        if self.start_time is None:
            self.start_time = datetime.now()
            # np.append(self.timestamps,get_time(t.timestamp))
            self.open=t.price
            self.low=t.price
            self.high=t.price


        if  datetime.now().minute>=(self.start_time.minute+1):
            self.close=t.price
            self.data_per_minute= np.append(self.data_per_minute,np.array([self.open,self.close,self.high,self.low,round(self.trade_volume/self.total_trades_per_minute,2)]))
            self.reset_values()
            self.reset_val_cond=True
        if datetime.now().minute>=(self.initial_start.minute+20):

            self.df = pd.DataFrame(self.data_per_minute.reshape(20,5), columns=['Open','Close','High','Low','avg_volume'])
            new_predictor= Predictor(self.df)
            for i in range(2,new_predictor.df.shape[0]-2):
                if new_predictor.get_Support(i)==True:
                    np.append(new_predictor.supports,new_predictor.df['Low'][i])
                elif new_predictor.get_Resistance(i)==True:
                    np.append(new_predictor.resistances,new_predictor.df['High'][i])
            print("Resistance: ")
            print(new_predictor.resistances)
            print("Supports: ")
            print(new_predictor.supports)
            np.savetxt('bars.csv',self.df)
            sys.exit()
        if self.reset_val_cond==False:
            if t.price>self.high:
                self.high = t.price
            if t.price<self.low:
                self.low=t.price
            self.total_trades_per_minute+=1
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
        print('trade', t)
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
    return time.time()


test_bot = Bot('AAPL')
test_bot.get_live_price_data('AAPL')
