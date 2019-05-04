from datetime import datetime, timedelta
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
from pytrends.request import TrendReq
import math
import pandas as pd
import requests as rq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib import style

style.use('ggplot')

#setting data age
today = datetime.today().strftime('%Y-%m-%d')
dataStart = datetime.today() - timedelta(days=90)
dataStartStr = dataStart.strftime('%Y-%m-%d')

#getting data
url = 'https://rest.coinapi.io/v1/ohlcv/BTC/USD/history?period_id=1DAY&time_start='+dataStartStr+'T00:00:00&time_end='+today+'T00:00:00'
headers = {'X-CoinAPI-Key' : 'A9FC5CDC-6195-4EAF-82A8-F8D776D432CD'}
response = rq.get(url, headers=headers)
df = pd.read_json(response.content)

#google trends data; only grabs up to 87 days so it must be formatted
fillUnavailabelData = pd.DataFrame({'Bitcoin':['NaN', 'NaN', 'NaN'], 'isPartial':[False, False, False]}) 
kw_list = ['Bitcoin']
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='', gprop='')
intrest = pytrends.interest_over_time()
intrest = intrest.append(fillUnavailabelData, ignore_index=True)
df['BTC_Intrest'] = intrest['Bitcoin']
df['BTC_Intrest'] = df['BTC_Intrest'].shift(3)
df.fillna(-99999, inplace=True)

#formatting dates to be cleaner
dates = []
for date in df['time_period_start']:
	temp = date.split('T')
	dates.append(temp[0])
df['time_period_start'] = dates

#reformat structure of data
df = df[['time_period_start', 'price_open', 'price_close', 'price_high', 'price_low', 'volume_traded', 'BTC_Intrest']]
df = df.set_index(df['time_period_start'])

#create labels
df['HL_pct'] = (df['price_high'] - df['price_low']) / df['price_high'] * 100.0
df['CH_pct'] = (df['price_close'] - df['price_open']) / df['price_close'] * 100.0
df['BTC_Intrest'] = df['BTC_Intrest'] / 100.0

#reformat structure of data
df = df[['price_close','HL_pct','CH_pct', 'BTC_Intrest', 'volume_traded']]

#column to predict
forecast_col = 'price_close'

#prediciting 10% of data length into future
forecast_out = int(math.ceil(0.1*len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

#defining model data
X = np.array(df.drop(['label'],1)) 
X_lately = X[-forecast_out:] 
X = X[:-forecast_out]

#defining model data
dfY = df.dropna()
y = np.array(dfY['label'])

#defining training and testing data
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

#training model, fit = training, score = testing
clf = LinearRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
forecast_set = clf.predict(X_lately)

#print(accuracy)

#column for predicted data
df['Forecast'] = np.nan

#formatting date for plotting
last_date = df.iloc[-1].name
last_date = datetime.strptime(last_date, '%Y-%m-%d')
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
	next_date = datetime.fromtimestamp(next_unix)
	next_date = next_date.strftime('%Y-%m-%d')
	next_unix += one_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

#plotting
plt.plot(df['price_close'], label = "Closing Price")
plt.plot(df['Forecast'])
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.gca().xaxis.set_major_locator(mticker.LinearLocator(18))
plt.gcf().autofmt_xdate(rotation=25)
plt.gcf().savefig('bitcoin_prediction.png')


