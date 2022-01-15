from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from alpaca_trade_api.stream import Stream
from datetime import datetime
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz

from company import Company
api = REST(key_id='AK6XD1EIN49YAJYBTSO8',secret_key='Wvdxl7a7oDlN0MBE7zkDzbg3SqHachg1cyyQn39i', api_version='v2')
stream = Stream(key_id='AK6XD1EIN49YAJYBTSO8',
                secret_key='Wvdxl7a7oDlN0MBE7zkDzbg3SqHachg1cyyQn39i',
                data_feed='sip')




fig = plt.figure()
ax = plt.axes()


df=api.get_bars('AAPL', TimeFrame.Minute, "2020-12-06", "2021-01-05", adjustment='raw').df
print(df)

df=pd.DataFrame(data=df,columns=['Open','Close','High','Low','avg_volume'])
print(df)
low=df['Low']
high=df['High']
print(low[0],high[0])
cycles=[]
for i in range(1,20):
    cycles.append(i)


plt.plot(cycles, low,label = "lows")
plt.plot(cycles, high,label = "highs")

plt.xlabel('cycles')
plt.ylabel('price for lows and highs')
plt.title('lows and highs', fontsize = 20)
plt.grid()
plt.legend()
plt.show()
