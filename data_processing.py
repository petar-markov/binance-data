import datetime
import json 
from itertools import combinations
from typing import Type
from generic_helpers import gen_dates_interval, last_day_of_month
from returns_statistics import sharpe_ratio, sortino_ratio
from math_helpers import correlation

def get_monthly_returns_and_statistics(start: str, 
                        end: str, 
                        file_name:str = '', 
                        save:bool = False, 
                        output_file_name:str = 'monthly_returns.json') -> dict:
    """
    params:
        start - begin of interval for 1M returns to compute, in format YYYY-MM-DD
        end - end of interval for 1M returns to compute, in format YYYY-MM-DD
        file_name - source file name. Should in the same (./) directory.
        save - save the 1M returns to a file on the file system.
        
    Compute the monthly returns for a given group of entities/cryptocurriencies from an input file.
    Output file with the 1M month returns is to be output and possible to be saved locally on the FS.
        
    """
    if file_name == '':
        raise ValueError('Please specify valid and existing file name.')

    with open(file_name) as f:
        ds = json.load(f)
    
    start = start.split('-')
    end = end.split('-')
    
    if (len(start[0]) != 4) or (len(end[0]) != 4):
        raise ValueError('Incorrect year format. Please provide a valid date, eg. 2021!')
    
    # First convert to datetime format then date only.
    # We need date only to use for indexing, but datetime first ensures, there will
    # be no problem with: 05 instead of 5, 02 instead of 2, etc. in the days/months.

    start = datetime.datetime(int(start[0]),int(start[1]),int(start[2])).date()
    end = datetime.datetime(int(end[0]),int(end[1]),int(end[2])).date()
        
    if start < datetime.date(2019, 12, 31):
        raise ValueError('Invalid start date provided. Start date must be >= 2019-12-31!')

    if end > datetime.date(2021, 5, 31):
        raise ValueError('Invalid end date provided. Start date must be <= 2021-05-31!')
    
    month_returns = {}
    all_correlations = {}
    
    for d in gen_dates_interval(start, end, datetime.timedelta(days=1)):
        prev_month_end = d.strftime('%Y-%m-%d')
        cur_month_end = last_day_of_month((d + datetime.timedelta(days=1))).strftime('%Y-%m-%d')
        
        for ccy in ds.keys():
            if ccy not in month_returns:
                month_returns[ccy] = []
            # Index is 3, since we moved the date outside of the data list
            try:
                a = float(ds.get(ccy).get(cur_month_end)[3])
                b = float(ds.get(ccy).get(prev_month_end)[3])
            except TypeError:
                raise TypeError('Something gone wrong when hitting a dictionary index. Check Dates!')
            if (not a or not b):
                break
            
            # Pretty much a simple arithmetic return calculation
            current_return = (a/b)-1
            # Because of how we iterate those should be always in ascending order
            # TODO: check for this...
            month_returns[ccy].append(current_return)
            
            try:
                sharpe = sharpe_ratio(month_returns[ccy], len(month_returns[ccy]))
                sortino = sortino_ratio(month_returns[ccy], len(month_returns[ccy]))
            except AssertionError:
                sharpe = 0
                sortino = 0
            print(f'1M Return for: {prev_month_end}, {cur_month_end}, {ccy}, {current_return}, Sharpe Ratio = {sharpe}, Sortino Ratio = {sortino}')
        
        pairs = [",".join(map(str, comb)) for comb in combinations(month_returns.keys(), 2)]
        if pairs:
            all_correlations[cur_month_end] = []
            for pair in pairs:
                a = pair.split(',')[0]
                b = pair.split(',')[1]
                try:
                    corr = correlation(month_returns[a], month_returns[b])
                    all_correlations[cur_month_end].append([pair, corr])
                except:
                    corr = 0.0
                    all_correlations[cur_month_end].append([pair, corr])
         
        print(f'Pair with max correlation as of {cur_month_end}: {sorted(all_correlations[cur_month_end], key = lambda x:x[1], reverse = True)[0]}')

    # If save option is enabled all results are saved to the FS
    # Even though the 2 files are JSON format, by definition the whole
    # output file will not be a valid JSON, because we dumpt both in the same file.
    # If this is processed/worked further, this has to be worked out.
    if save:
        with open(output_file_name, 'w') as f:
            json.dump(month_returns, f)
            json.dump(all_correlations, f)

    return month_returns, all_correlations