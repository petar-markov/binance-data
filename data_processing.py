import datetime
import json 
from itertools import combinations
from typing import Type
from generic_helpers import gen_dates_interval, last_day_of_month
from returns_statistics import sharpe_ratio, sortino_ratio
from math_helpers import correlation, rankdata

def get_monthly_returns_and_statistics(start: str, 
                        end: str, 
                        file_name:str = '', 
                        save:bool = False) -> dict:
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
        raise ValueError('Invalid end date provided. End date must be <= 2021-05-31!')
    
    month_returns = {}
    market_cap_series = {}
    rank_corr_coef_results = {}
    all_correlations = {}
    all_stats = {}
    
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

            # Sharpe and Sortino ratios calculated in here
            try:
                sharpe = sharpe_ratio(month_returns[ccy], len(month_returns[ccy]))
            except AssertionError:
                sharpe = 0
                
            try:
                sortino = sortino_ratio(month_returns[ccy], len(month_returns[ccy]))
            except AssertionError:
                sortino = 0

            # Rank correlation starting in here
            # Custom functions used, but the final results verified against
            # scipy.stats.spearmanr and give pretty much the same results
            if ccy not in market_cap_series:
                market_cap_series[ccy] = []
            if ccy not in rank_corr_coef_results:
                rank_corr_coef_results[ccy] = []
            
            mk = float(ds.get(ccy).get(cur_month_end)[-1])
            market_cap_series[ccy].append(mk)

            ranked_returns = rankdata(month_returns[ccy])
            ranked_market_cap = rankdata(market_cap_series[ccy])
            try:
                rank_corr_coef = correlation(ranked_returns, ranked_market_cap)
            except AssertionError:
                rank_corr_coef = 0
            
            rank_corr_coef_results[ccy].append(rank_corr_coef)
            
            # Add all the monthly data for the current crypto in a mutual dataset to be returned later
            all_stats[cur_month_end] = [ccy, current_return, sharpe, sortino, rank_corr_coef]
            print(f'1M Return for: {prev_month_end}, {cur_month_end}, {ccy}, {current_return}, Sharpe Ratio = {sharpe}, Sortino Ratio = {sortino}, Rank corr. coef (market cap vs. return) = {rank_corr_coef}')


        # Correlation between the pairs' returns starting in here        
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
    # 2 files are output, both in JSON format,
    # first one has all monthly based statistics and the second one has all the
    # pairs' returns correlations
    if save:
        with open('all_stats.json', 'w') as f0, open('pairs_returns_correlations.json', 'w') as f1:
            json.dump(all_stats, f0)
            json.dump(all_correlations, f1)

    return all_stats, all_correlations
