#Imports
from datetime import datetime, timedelta
import requests as rq
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib import style 

#Stop warinngs, no idea what it does
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#Get dates to search data by
today = datetime.today().strftime('%Y-%m-%d')
dataStart = datetime.today() - timedelta(days=90)
dataStartStr = dataStart.strftime('%Y-%m-%d')

#Get price data from API
url = 'https://rest.coinapi.io/v1/ohlcv/BTC/USD/history?period_id=1DAY&time_start='+dataStartStr+'T00:00:00&time_end='+today+'T00:00:00'
headers = {'X-CoinAPI-Key' : 'A9FC5CDC-6195-4EAF-82A8-F8D776D432CD'}
response = rq.get(url, headers=headers)
df = pd.read_json(response.content)


#Conver dates to Matplotlib readable format
datesDirty = []
for date in df["time_period_start"]:
	datesDirty.append(date.split('T')[0])

datesClean = mdates.datestr2num(datesDirty)
closep = df["price_close"]
openp = df["price_open"]
highp = df["price_high"]
lowp = df["price_low"]
volume = df["volume_traded"]

#Plot and save graph
style.use('ggplot')

fig = plt.figure()

x = 0
y = len(datesClean)-1
ohlc = []

while x < y:
	append_me = datesClean[x], openp[x], highp[x], lowp[x], closep[x]
	ohlc.append(append_me)
	x+=1

ax1 = plt.subplot2grid((1,1),(0,0))
candlestick_ohlc(ax1, ohlc, width=0.4, colorup='g', colordown='r')

plt.gcf().autofmt_xdate(rotation=25)
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

plt.ylim(min(closep)-100, max(closep)+100)
plt.xlabel("Day of Close")
plt.ylabel("Bitcoin Closing Price")
plt.title("Bitcoin Data\n90 days")

fig.savefig('bitcoin_graph.png')
