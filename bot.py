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
from company import Company
from tda import auth, client
import tda_config
from tda.orders.common import Duration, Session




#alpaca setup
api = REST(key_id='PK6DTGDMQWC6O7T67JK1',secret_key='PqOMzUcVQTtlTZYKNK0idzyfptA9OorZq7SGn00w', base_url='https://paper-api.alpaca.markets', api_version='v2')
account=api.get_account()
stream = Stream(key_id='AK6XD1EIN49YAJYBTSO8',
                secret_key='Wvdxl7a7oDlN0MBE7zkDzbg3SqHachg1cyyQn39i',
                data_feed='sip')


#tda setup
try:
    c = auth.client_from_token_file(tda_config.token_path, tda_config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='/Users/arvinseifipour/dev/signal/chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, tda_config.api_key, tda_config.redirect_uri, tda_config.token_path)
target_date= datetime.strptime('2022-01-19','%Y-%m-%d').date()
print(target_date)
# r = c.get_option_chain('AAPL',contract_type=c.Options.ContractType.CALL, strike=300, startDate= target_date,endDate= target_date)
#
# print(json.dumps(r.json(), indent=4))



class Bot:

    def __init__(self, stocks_to_watch):
        self.stocks_to_watch = stocks_to_watch
        self.companies= {}
        self.initial_start = datetime.now()
        self.time_increment=self.initial_start
        self.curr_avg_trade_volumes=[]
        self.data_per_minute= np.array([])
        self.prices=[]
        self.start_time = None
        self.reset_val_cond=False
        self.df=None
        self.data_collected = False



    def setup(self):
        self.initialize_companies()
        self.get_historical_price_data()
        self.get_thirty_day_avg_volume()


    def initialize_companies(self):
        for stock in self.stocks_to_watch:
            self.companies[stock]=Company(stock)


    def get_historical_price_data(self):
        # now = pd.Timestamp.now(tz='US/Pacific').floor('1min')
        # today = now.strftime('%Y-%m-%d')
        # tomorrow = (now + pd.Timedelta('1day')).strftime('%Y-%m-%d')
        # bar = api.get_barset([company], 'minute', start=today, end=tomorrow).df

        for company in self.companies.keys():

            self.companies[company].thirty_day_df =api.get_bars(company, TimeFrame.Minute, "2021-12-11", "2022-01-11", adjustment='raw').df

    def test_on_historical_data(self):

        self.get_historical_price_data()

        for company in self.companies.keys():

            self.companies[company].daily_df = api.get_bars(company, TimeFrame.Minute, "2022-01-06", "2022-01-06").df
            self.companies[company].daily_df= self.companies[company].daily_df.reset_index()

        for company in self.companies.keys():

            self.companies[company].predictor = Predictor(self.companies[company].daily_df)


    def get_thirty_day_avg_volume(self):
        for company in self.companies.keys():
            self.companies[company].thirty_day_avg_vol = sum(self.companies[company].thirty_day_df.volume)/sum(self.companies[company].thirty_day_df.trade_count)


    def signal_breakout(self,resistance,support,price):
        if price<support:
            return 's'
        if price>resistance:
            return 'r'

    def signal_buy_sell(self,price,resistance,support,curr_volume,thirty_day_avg_volume):

        if self.signal_breakout(resistance,support,price)=='r':
            if curr_volume>=thirty_day_avg_volume*0.6:
                return 'buy'
        if self.signal_breakout(resistance,support,price)=='s':
            if curr_volume>=thirty_day_avg_volume*0.3:
                return 'sell'
        else:
            return None

    def get_quantity(self, most_expensive_ticker,t_price):

        quantity = 10
        max_temp_price = self.companies[most_expensive_ticker].prices[len(self.companies[most_expensive_ticker].prices)-1] * 10
        quantity = int(max_temp_price/t_price)
        return quantity


    def get_bars(self,t):
        curr_company = t.symbol
        if self.data_collected==True:
            self.initial_start= datetime.now()
            self.data_collected=False
        if self.start_time is None and self.reset_val_cond==True:
            self.reset_val_cond=False

        if self.start_time is None:
            self.start_time = datetime.now()
            # np.append(self.timestamps,get_time(t.timestamp))
        if self.companies[curr_company].open==0:
            self.companies[curr_company].open=t.price

        #check if initial data is collected and make signals
        if self.companies[curr_company].daily_df.empty!=True:
            self.companies[curr_company].signal = self.signal_buy_sell(t.price,max(self.companies[curr_company].predictor.resistances),min(self.companies[curr_company].predictor.supports),t.size,self.companies[curr_company].thirty_day_avg_vol)

            if self.companies[curr_company].signal is not None:
                print(self.companies[curr_company].signal,curr_company)


            #buy calls
            # if self.companies[curr_company].signal == 'buy':
            #     if self.companies[curr_company].in_position_calls==False:
                    # quantity= self.get_quantity('TSLA',t.price)
                    # self.companies[curr_company].share_numbers=quantity
                    # api.submit_order(
                    #     symbol= curr_company,
                    #     side='buy',
                    #     type='market',
                    #     qty= quantity,
                    #     time_in_force='day'
                    # )
                    #to-do: place buy order for call
                    # self.companies[curr_company].in_position_calls = True
                    # self.companies[curr_company].calls_bought_at = t.price

            #sell profits when value keeps going up
            # if self.companies[curr_company].signal == 'buy' and self.companies[curr_company].in_position_calls == True and self.profit_loss>=(self.companies[curr_company].initial_investment*2.1):
                # api.submit_order(
                #     symbol= curr_company,
                #     side='sell',
                #     type='market',
                #     qty=self.companies[curr_company].share_numbers,
                #     time_in_force='day'
                # )
                #to-do: place sell order for calls
                # self.companies[curr_company].in_position_calls = False


            #sell loss or profit when market stagnant
            # if  self.companies[curr_company].signal == None:
            #     if self.companies[curr_company].in_position_calls == True:
            #         if self.profit_loss>=(self.companies[curr_company].initial_investment*1.1)  or self.profit_loss<=(self.companies[curr_company].initial_investment*0.8) :

                        # api.submit_order(
                        #     symbol= curr_company,
                        #     side='sell',
                        #     type='market',
                        #     qty= self.companies[curr_company].share_numbers,
                        #     time_in_force='day'
                        # )
                        #to-do: place sell order for calls
                        # self.companies[curr_company].in_position_calls = False
            #sell calls when maket drops below support
            # if self.companies[curr_company].signal == 'sell':
            #     if self.companies[curr_company].in_position_calls == True:
                    # api.submit_order(
                    #     symbol= curr_company,
                    #     side='sell',
                    #     type='market',
                    #     qty=self.companies[curr_company].share_numbers,
                    #     time_in_force='day'
                    # )
                    #to-do:place sell order for calls
                    # self.companies[curr_company].in_position_calls = False
            #buy puts when market about to drop
            # if self.companies[curr_company].signal == 'sell':
            #     if self.companies[curr_company].in_position_puts == False:
                    #todo: place order to buy puts

                    # self.companies[curr_company].in_position_puts = True
                    # self.companies[curr_company].puts_bought_at = t.price

            #sell puts when market stagnant
            # if self.companies[curr_company].signal == None:
            #     if self.companies[curr_company].in_position_puts == True:
            #         if self.profit_loss>=(self.companies[curr_company].initial_investment*1.1)  or self.profit_loss<=(self.companies[curr_company].initial_investment*0.8) :
            #             #todo:place order to sell puts
            #             self.companies[curr_company].in_position_puts == False
            #
            #
            # #sell puts profit when market keeps going down
            # if self.companies[curr_company].signal == 'sell' and self.companies[curr_company].in_position_puts == True and self.profit_loss>=(self.companies[curr_company].initial_investment*2.1):
            #     #todo:place order to sell puts
            #     self.companies[curr_company].in_position_puts == False
            #
            # #sell puts when market takes off above resistance
            # if self.companies[curr_company].signal == 'buy':
            #     if self.companies[curr_company].in_position_puts == True:
            #         #to-do:place sell order for calls
            #         self.companies[curr_company].in_position_puts = False


        if datetime.now().minute>=(self.start_time.minute+1):
            for company in self.companies.keys():
                self.companies[company].timestamps=t.timestamp
                self.companies[company].close=self.companies[company].prices[len(self.companies[company].prices)-1]
                self.companies[company].data_per_minute= np.append(self.companies[company].data_per_minute,np.array([self.companies[company].timestamps,self.companies[company].open,self.companies[company].close,self.companies[company].high,self.companies[company].low]))
                self.companies[company].curr_avg_volume = self.companies[company].trade_volume/self.companies[company].total_trades_per_minute
                self.companies[company].curr_avg_trade_volumes.append(self.companies[company].curr_avg_volume)
            print("got to here")

            self.reset_values()

            self.reset_val_cond=True
        if datetime.now().minute>=(self.initial_start.minute+5):
            for company in self.companies.keys():
                self.companies[company].daily_avg_volume=(sum(self.companies[company].curr_avg_trade_volumes)/len(self.companies[company].curr_avg_trade_volumes))
                try:
                    self.companies[company].minute_df = pd.DataFrame(self.companies[company].data_per_minute.reshape(5,5), columns=['Timestamp','Open','Close','High','Low'])
                except ValueError:
                    self.companies[company].minute_df = pd.DataFrame(self.companies[company].data_per_minute.reshape(4,5), columns=['Timestamp','Open','Close','High','Low'])    
                updated_frame_data = [self.companies[company].daily_df,self.companies[company].minute_df]
                self.companies[company].daily_df=pd.concat(updated_frame_data)
                self.companies[company].daily_df=self.companies[company].daily_df.reset_index(drop=True)
            print(self.companies['AAPL'].daily_df)
            for company in self.companies.keys():

                self.companies[company].predictor= Predictor(self.companies[company].daily_df)
                lows = pd.DataFrame(data=self.companies[company].daily_df, index=self.companies[company].daily_df.index, columns=["Low"])
                highs = pd.DataFrame(data=self.companies[company].daily_df, index=self.companies[company].daily_df.index, columns=["High"])

                self.companies[company].predictor.predict_resistance(highs)
                self.companies[company].predictor.predict_support(lows)


                print("Resistance: ")
                print(self.companies[company].predictor.resistances)
                print("Supports: ")
                print(self.companies[company].predictor.supports)
            print("got to here too")


            self.reset_values()
            self.data_collected=True
            for company in self.companies.keys():
                self.companies[company].data_per_minute= np.array([])

        if self.reset_val_cond==False:
            if t.price>self.companies[curr_company].high:
                self.companies[curr_company].high = t.price
            if self.companies[curr_company].low is None:
                self.companies[curr_company].low=t.price
            if t.price<self.companies[curr_company].low:
                self.companies[curr_company].low=t.price
            self.companies[curr_company].total_trades_per_minute+=1
            if t.size!=0:
                self.companies[curr_company].trade_volume+=t.size
            self.companies[curr_company].prices.append(t.price)

    def reset_values(self):
        for company in self.companies.keys():
            self.companies[company].high=0
            self.companies[company].low=None
            self.companies[company].open=0
            self.companies[company].close=0
            self.companies[company].total_trades_per_minute=0
            self.companies[company].trade_volume=0
        self.start_time=None

    def get_live_price_data(self):
        for stock in self.stocks_to_watch:
            stream.subscribe_trades(self.trade_callback,stock)
        stream.run()
    async def trade_callback(self,t):

        self.get_bars(t)




pst= pytz.timezone('US/Pacific')
def get_time(unix_epoch_time):
    my_datetime = str(pd.to_datetime(unix_epoch_time, unit='ns', utc=True))

    time= datetime((int(my_datetime[0:4])),(int(my_datetime[5:7])),(int(my_datetime[8:10])),(int(my_datetime[11:13])),(int(my_datetime[14:16])),(int(my_datetime[17:19])))

    return time.time

def run_forever():
    try:
        test_bot = Bot(['AAPL','AMD','TSLA','QQQ','NVDA','PYPL','F','SNAP'])
        test_bot.setup()
        test_bot.get_live_price_data()
    except ValueError:
        run_forever()

run_forever()
