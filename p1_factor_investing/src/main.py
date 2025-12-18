# import the usual 
import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm


def main():
    # Load the data
    tickers = ["SPY"]
    data = yf.download(tickers, start="2015-01-01")["Adj Close"]
    data = data.dropna()
    returns = data.pct_change().dropna()

    # We will explore a popular momentum factor effect of past 12 months - 1
    # aka 12 minus 1 factor effect: https://quantpedia.com/strategies/momentum-factor-effect-in-stocks
    r = returns["SPY"]

    # 252 trading days - 21 (1 month)
    # this is the momentum factor definition (momentum_i = product of (1 + r) - 1)
    momentum = (1 + r.shift(21)).rolling(252).apply(np.prod, raw=True) - 1

    
    # Then we will explore volatility, and specifically a rolling beta regression
    # first we will do a regular linear regression to find the beta (slope)

    volatility = r.rolling(252).std()


    # Then we will take a rolling beta regression, so do the same thing as above but slide it by 1 day and recalculate, etc
    # We calculate the beta by doing an OLS (least squares linear regression)

    market_r = returns["SPY"]
    rb = rolling_beta(r, market_r) 

def rolling_beta(asset, market, window=252):
    betas = []
    idx = []
    for i in range(window, len(asset)):
        y = asset.iloc[i-window:i]
        X = sm.add_constant(market.iloc[i-window:i])
        beta = sm.OLS(y, X).fit().params[1]
        betas.append(beta)
        idx.append(asset.index[i])
    return pd.Series(betas, index=idx)

beta = rolling_beta(r, market_r)



if __name__ == "__main__":
    main()