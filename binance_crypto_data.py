from generic_helpers import get_top_cryptoccy_by_market_cap
from load_data import load_data
from data_processing import get_monthly_returns_and_statistics

# Get the top 20 cryptos by market cap
# Cryptos and market cap is retrieved + cryptos only. Second one is for easier further usage.
cryptos_market_cap, cryptos_only = get_top_cryptoccy_by_market_cap(20)
print(cryptos_market_cap)

# Load the data from Binance API and save locally on the FS.
# File is loaded in the folder where this is executed.
# TODO- further improvement is to specify explicitly the full path where the file is saved.
dataset = load_data(
    cryptos = cryptos_only, 
    start = '2019-12-31', 
    end = '2021-6-4', 
    frequency = '1d', 
    limit = 1000, 
    file_name = 'binance_crypto_data.json'
    )


# Get some work done with the loaded data.
# Current state of this function covers monthly returns, sharpe ratio and sortino ratio
# TODO implement rank correlation between the market cap and returns - again on monthly basis.
# Monthly Returns and All pair correlations are saved in variables and dumped into a file on the FS.
# Monthly stats are being printed.
monthly_returns, all_pair_correlations = get_monthly_returns_and_statistics(start = '2019-12-31', 
                                                                            end = '2021-5-31', 
                                                                            file_name = 'binance_crypto_data.json', 
                                                                            save = True, 
                                                                            output_file_name = 'results')

