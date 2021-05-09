import time
import pyupbit
import datetime

access = "accesskey "
secret = "secretkey"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=1)
    start_time = df.index[0]
    return start_time

def get_ma12(ticker):
    """12시간 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=12)
    ma12 = df['close'].rolling(12).mean().iloc[-1]
    return ma12

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

 # 자동매매 시작
while True:
     try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(minutes=10)

        if start_time < now < end_time - datetime.timedelta(seconds=1):
             print(1)
             target_price = get_target_price("KRW-ETH", 0.5)
             ma12 = get_ma12("KRW-ETH")
             current_price = get_current_price("KRW-ETH")
             print(target_price,ma12,current_price)
             if target_price < current_price and ma12 < current_price:
                 print(2)
                 krw = get_balance("KRW")
                 if krw > 10000:
                     print(3)
                     upbit.buy_market_order("KRW-ETH", 10000*0.9995)
        else:
             eth = get_balance("ETH")
             if eth > 0.00008:
                 print(4)
                 upbit.sell_market_order("KRW-ETH", eth*0.9995)
        time.sleep(1)
     except Exception as e:
         print(e)
         time.sleep(1)
