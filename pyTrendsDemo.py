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

today = datetime.today().strftime('%Y-%m-%d')
dataStart = datetime.today() - timedelta(days=90)
dataStartStr = dataStart.strftime('%Y-%m-%d')

range = today + " " + dataStartStr
print(range)

url = 'https://rest.coinapi.io/v1/ohlcv/BTC/USD/history?period_id=1DAY&time_start='+dataStartStr+'T00:00:00&time_end='+today+'T00:00:00'
headers = {'X-CoinAPI-Key' : 'A9FC5CDC-6195-4EAF-82A8-F8D776D432CD'}
response = rq.get(url, headers=headers)
df = pd.read_json(response.content)

fillUnavailabelData = pd.DataFrame({"Bitcoin":['NaN', 'NaN', 'NaN'], "isPartial":[False, False, False]}) 
#print(newDataFrame)

kw_list = ['Bitcoin']
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='', gprop='')
intrest = pytrends.interest_over_time()
intrest = intrest.append(fillUnavailabelData, ignore_index=True)
df['BTC_Intrest'] = intrest["Bitcoin"]
df['BTC_Intrest'] = df['BTC_Intrest'].shift(3)
df['BTC_Intrest'] = df['BTC_Intrest'] / 100.0
df.fillna(-99999, inplace=True)
print(df)