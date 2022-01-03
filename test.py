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


test_bot = Bot('AAPL')
hist_price= test_bot.get_historical_price_data('AAPL')
print(hist_price.shape)
df = pd.DataFrame(data=hist_price['AAPL'])
df=df.reset_index()
print(df)




def get_optimum_clusters(df, saturation_point=0.05):

    wcss = []
    k_models = []

    size = min(11, len(df.index))
    for i in range(1, size):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(df)
        wcss.append(kmeans.inertia_)
        k_models.append(kmeans)

    # Compare differences in inertias until it's no more than saturation_point
    optimum_k = len(wcss)-1
    for i in range(0, len(wcss)-1):
        diff = abs(wcss[i+1] - wcss[i])
        if diff < saturation_point:
            optimum_k = i
            break

    print("Optimum K is " + str(optimum_k + 1))
    optimum_clusters = k_models[optimum_k]

    return optimum_clusters


print(len(df['low']))

lows = pd.DataFrame(data=df, index=df.index, columns=["low"])
highs = pd.DataFrame(data=df, index=df.index, columns=["high"])

low_clusters = get_optimum_clusters(lows)
low_centers = low_clusters.cluster_centers_
low_centers = np.sort(low_centers, axis=0)

high_clusters = get_optimum_clusters(highs)
high_centers = high_clusters.cluster_centers_
high_centers = np.sort(high_centers, axis=0)
print(low_centers)
print("-----------")
print(high_centers)

def plot_stock_data(data):
    fig, ax = plt.subplots()
    ax1 = plt.subplot2grid((5,1), (0,0), rowspan=4)
    ax2 = plt.subplot2grid((5,1), (4,0), sharex=ax1)

    ax1.set_title("{}".format('AAPL'))
    ax1.set_facecolor("#131722")
    ax1.xaxis.set_major_formatter(mpticker.FuncFormatter(mydate))

    candlestick_ohlc(ax1, data.to_numpy(), width=8, colorup='#77d879', colordown='#db3f3f')

    ax2.bar(data['time'], width=30)
    ax2.xaxis.set_major_formatter(mpticker.FuncFormatter(mydate))
    fig.subplots_adjust(hspace=0)
    fig.autofmt_xdate()
    return ax1


def mydate(x,pos):
    try:
        return datetime.fromtimestamp(x).strftime('%H:%M')
    except IndexError:
        return ''

plt.style.use('ggplot')
ax = plot_stock_data(df)

# Extracting Data for plotting
# df['time']=df['time'].apply(lambda x:datetime.fromtimestamp(x).strftime('%H:%M'))
ohlc = df.loc[:, ['time','open', 'high', 'low', 'close']]
ohlc = ohlc.astype(float)

# Creating Subplots
fig, ax = plt.subplots()

candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

# Setting labels & titles
fig.suptitle('Daily Candlestick Chart')
for low in low_centers[:2]:
    ax.axhline(low[0], color='yellow', ls='--')

for high in high_centers[-1:]:
    ax.axhline(high[0], color='orange', ls='--')

plt.show()

# Formatting Date

fig.tight_layout()

plt.show()
