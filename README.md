# binance-data

Simple code to get some basic data from the public Binance API and calculate some statistics one them.

Example output files available (from an already completed execution):
  - pairs_returns_correlations.json - All the correlation coefficients for all the cryptocurrency pairs. If N=20, 20 distinct cryptocurrencies will be used in here.
  - binance_crypto_data.json - Initial data for all the cryptocurrencies received from the Binance API. Endpoint used: https://api.binance.com/api/v3/klines
  - all_stats.json - Output file with all the calculations as of every month ends that we iterate through - Return, Sharpe & Sortino Ratio, Rank Correlation Coefficient from Market Cap vs. Return.


File to be called for the end to end execution - binance_crypto_data.py. As of now the way how this is called is not parametrized, so in case of input parameters that need to be modified (for example amount of cryptocurrencies), this has to be defiend in the file itself.


Other files:
  - generic_helpers.py - Has generic helper functions used, including the initial call to get top N cryptos based on their market cap. Other functions in there will help for fixing epoch time to a string formatted date, function to get the last date of the month, function to generate date intervals.
  - math_helpers.py - Has the math functions used/needed for the statistics and calculations. Those are ones to help for getting the correlation, rank correlation, some list operations.
  - returns_statistics.py - Has both the Sharpe and Sortino Ratio fucntions/logics.
  - load_data.py - Has the logic to load the initial data for N given entities, using the Binance API endpoing "klines". Returns a dataset structured in a JSON format, where against every cryptocurrency, for every day, we have the data in a list. For example:
  """
            {
      "BTC": {
          "2019-12-31": ["7246.00000000", "7320.00000000", "7145.01000000", "7195.23000000", "25954.45353300", 1577836799999, "187518399.34504001", 251976, "12595.93034700",      "91036201.13783441", "0", 134775601570.89]
          }
      }
  """
  - data_processing.py - Has all the logic for the different statistics, returns and correlations. All the cryptocurrencies are processed in here and finally we print the results as of every month end + we output the 2 results files.




