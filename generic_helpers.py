import requests
import json
from typing import List
import datetime

def get_top_cryptoccy_by_market_cap(n:int = 20) -> List[list]:
    """
    params:
        n - number of top crypto currencies by market cap to be extracted
    
    Extracts cryptocurrency tickers, by market cap, taking the top "n".
    For some reason the market cap is not that easy to find with the Binance API.
    This is a custom function on how to get top(n) crytocurrencies, compared on their market cap.
    
    """

    # Define to have at least 1 crypto to be extracted
    assert n > 0

    url = "https://www.binance.com/exchange-api/v2/public/asset-service/product/get-products"
    res = requests.get(url, verify=False)
    if res.status_code != 200:
        raise Exception(f'Something went wrong with the GET request. MSG: {res.text}')

    res_json = json.loads(res.text)
    
    crypto_ccys = []
    
    for item in res_json.get('data'):
        pair = item.get('s')
        if pair:
            if pair[-4:] != 'USDT':
                continue
        else:
            continue
            
        ticker = item.get('b')
        current_price = float(item.get('c'))
        supply = item.get('cs')
        if supply:
            supply = float(supply)
        else:
            continue
        
        market_cap = supply*current_price
        crypto_ccys.append([ticker, market_cap, supply])
        
        # Python's default sorting should work not that bad for this case. 
        crypto_ccys = sorted(crypto_ccys, key = lambda x:x[1], reverse = True)[:n]
    
    # Returning full data - with the market cap and supply included included in the format of a nested list.
    # Supply can be accessed and worked with further so that we calculate market cap using different prices.
    # Also returning the cryptocurrencies names only in list format, so that can be passed easily further
    # return crypto_ccys, [x[0] for x in crypto_ccys]
    return crypto_ccys


def fix_time(epoch_num:int) -> str:
    """
    Small function to convert epoch time in ms to a str representation of the actual date.
    Binance APIs provide the date/time format in epoch which is not that easily readable.
    
    """
    s = epoch_num / 1000
    return datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d')


def last_day_of_month(any_day):
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)


def gen_dates_interval(start, end, delta):
    curr = last_day_of_month(start)
    while curr < end:
        yield curr
        curr += delta
        curr = last_day_of_month(curr)
