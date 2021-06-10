import datetime
import json 
import requests
from generic_helpers import fix_time
from typing import List

def load_data(cryptos:List[list], 
               start:str, 
               end:str, 
               frequency:str = '1d', 
               limit:int = 1000, 
               file_name:str = 'binance_data.json') -> dict:
    """
    params:
        cryptos - dictionary of crypto currencies to extract data for, together with their market cap and supply
        start - begin of interval, in format YYYY-MM-DD
        end - end of interval, in format YYYY-MM-DD
        frequency - frequency to extract the data for, eg. every 1d, 1h, etc.
        limit - the API has a limit of 1000 datapoint for response. TODO if that is exceeded.
        file_name - Fesired name of a file to be saved locally.
        
    The API used in this functoin has a limitation of the amount of data points to be extracte.
    By default it is set to 500, so we increase that by default to 1000 for this function. Taking into
    account the requirements, 1000 data points for 1D data is all enough for interval starting in beginning
    of 2020, till mid 2021. In case that is used for larger periods/more granular time poitns, a functionality
    to iterate and load this correctly has to be implemented!

    Extract data from the binance public API based on a given cryptocurrency and interval.
    Output/payload should be as follow:
        [
      [
        1499040000000,      // Open time
        "0.01634790",       // Open
        "0.80000000",       // High
        "0.01575800",       // Low
        "0.01577100",       // Close
        "148976.11427815",  // Volume
        1499644799999,      // Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "17928899.62484339" // Ignore.
      ]
    ]
    
    """
    
    dataset = dict()
    
    start = start.split('-')
    end = end.split('-')
    url = "https://api.binance.com/api/v3/klines"
    if (len(start[0]) != 4) or (len(end[0]) != 4):
        raise ValueError('Incorrect year format. Please provide a valid date, eg. 2021!')

    if datetime.datetime(int(start[0]),int(start[1]),int(start[2])) < datetime.datetime(2019, 12, 31):
        raise ValueError('Invalid start date provided. Start date must be >= 2019-12-31!')
    start = int(datetime.datetime(int(start[0]),int(start[1]),int(start[2])).timestamp()*1000)

    # This is as of the time of dev of this function
    if datetime.datetime(int(end[0]),int(end[1]),int(end[2])) > datetime.datetime(2021, 6, 10):
        raise ValueError('Invalid end date provided. Start date must be <= 2021-06-10!')
    end = int(datetime.datetime(int(end[0]),int(end[1]),int(end[2])).timestamp()*1000)
    
    # Iteration over the cryptocurrencies only. 
    # From the input date we need to access later the supply to get the monthly market cap,
    # but this can be done directly with hitting the value by index.
    for i, ccy in enumerate([x[0] for x in cryptos]):
        staging_ds = dict()
        params = {
            'symbol': ccy+'USDT',
            'interval': frequency,
            'startTime': start,
            'endTime': end,
            'limit': 1000
        }

        res = requests.get(url, params=params, verify=False)
        if res.status_code != 200:
            raise Exception(f'Something went wrong with the GET request. MSG: {res.text}')

        data = json.loads(res.text)

        # Fix the epoch date and convert to a more structure dictionary
        for d in data:
            datestamp = fix_time(d[0])
            staging_ds[datestamp] = d[1::]
            supply = float(cryptos[i][2])
            price = float(d[4])
            market_cap = price * supply 
            staging_ds[datestamp].append(market_cap)
        
        # Finally add the data for this crypto ccy in the dictionary
        dataset[ccy] = staging_ds
    
    # Write the data to a file on the local FS. 
    with open(file_name, 'w') as f:
        json.dump(dataset, f)
        
    print(f'Data loaded. File {file_name} saved on FS.')
    return dataset
