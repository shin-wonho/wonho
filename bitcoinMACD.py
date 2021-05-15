import requests
import pandas as pd
import time
# import webbrowser
import pyupbit
import datetime

access = ""
secret = ""

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def record_trading(trade):
    current = datetime.datetime.now()
    current_time = current.replace(microsecond=0)
    t_current_time = current_time.strftime('%c')
    f = open('C:/crytoauto/record.txt', 'a')
    # 파일에 텍스트 쓰기
    f.writelines(["\ntime : ", t_current_time])
    f.writelines(["\nCall : ", call])
    f.close()


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

buy_flag = 0

while True:
    try:
        url = "https://api.upbit.com/v1/candles/minutes/10"

        querystring = {"market":"KRW-ETH","count":"100"}
      
        response = requests.request("GET", url, params=querystring)
      
        data = response.json()
      
        df = pd.DataFrame(data)
   
        df=df.iloc[::-1]

        df=df['trade_price']
        # print(df)
        # print(df[0])
        exp1 = df.ewm(span=12, adjust=False).mean()
        exp2 = df.ewm(span=26, adjust=False).mean()
        macd = exp1-exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
      
       #  print('MACD: ',macd[0])
       #  print('Signal: ',exp3[0])
      
        test1=macd[0]-exp3[0]
        test2=macd[1]-exp3[1]
      
        call='매매 필요없음'
    #    krw = get_balance("KRW")
    #    print(krw)
        if test1<0 and test2>=0 and buy_flag == 2:
            call='매도1'
            eth = get_balance("ETH")
            if eth > 0.00106:
                upbit.sell_market_order("KRW-ETH", eth*0.9995)
                buy_flag = 0
                record_trading(call)

        if test1<test2 and buy_flag == 1:
            call='매도2'
            eth = get_balance("ETH")
            if eth > 0.00106:
                upbit.sell_market_order("KRW-ETH", eth*0.9995)
                buy_flag = 0
                record_trading(call)
         
        if test1>0 and test2<=0 and buy_flag == 0:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-ETH", 10000*0.9995)
                record_trading(call)
                if macd[0] < 0:
                    call='매수1'
                    buy_flag = 1
                else:
                    call='매수2'
                    buy_flag = 2 
            record_trading(call)

        print('BTC 매매의견: ', call, buy_flag)

        time.sleep(1)

    except Exception as e:
       print(e)
       time.sleep(1)