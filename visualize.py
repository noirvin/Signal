import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



fig = plt.figure()
ax = plt.axes()


df=pd.read_csv('bars.csv')
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
