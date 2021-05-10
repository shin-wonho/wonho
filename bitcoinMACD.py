import requests
import pandas as pd
import time
# import webbrowser
import pyupbit

access = ""
secret = ""

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
       url = "https://api.upbit.com/v1/candles/minutes/10"

       querystring = {"market":"KRW-ETH","count":"100"}
      
       response = requests.request("GET", url, params=querystring)
      
       data = response.json()
      
       df = pd.DataFrame(data)
   
       df=df.iloc[::-1]

       df=df['trade_price']

       exp1 = df.ewm(span=12, adjust=False).mean()
       exp2 = df.ewm(span=26, adjust=False).mean()
       macd = exp1-exp2
       exp3 = macd.ewm(span=9, adjust=False).mean()
      
       #  print('MACD: ',macd[0])
       #  print('Signal: ',exp3[0])
      
       test1=macd[0]-exp3[0]
       test2=macd[1]-exp3[1]
      
      #  call='매매 필요없음'
      
       if test1<0 and test2>0:
         #  call='매도'
          eth = get_balance("ETH")
          if eth > 0.00106:
             upbit.sell_market_order("KRW-ETH", eth*0.9995)
         
       if test1>0 and test2<0:
         #  call='매수'
          krw = get_balance("KRW")
          if krw > 5000:
             upbit.buy_market_order("KRW-ETH", 10000*0.9995)
      #  print('BTC 매매의견: ', call)

       time.sleep(1)

    except Exception as e:
       print(e)
       time.sleep(1)


